import wikipedia # Python Wikipedia library (or similar)
# Potentially import NLP libraries like NLTK or spaCy if you go deeper

class WikipediaFlashcardAgent:
    def __init__(self, language="en"):
        wikipedia.set_lang(language)
        self.page = None # Initialize page attribute
        # You might initialize NLP models here if using them

    def generate_flashcards(self, topic: str, num_cards_desired: int = 10, strategies: list = None):
        """
        Main agentic function to generate flashcards for a given topic.
        Strategies could be ['summary', 'infobox', 'headings_detailed', 'key_concepts']
        """
        if strategies is None:
            strategies = ['summary', 'headings_detailed'] # Default strategies

        flashcards = []
        
        try:
            # Step 1: Find the right Wikipedia page (handles disambiguation to some extent)
            page_title_search = wikipedia.search(topic, results=1)
            if not page_title_search:
                print(f"Could not find a Wikipedia page for '{topic}'")
                return []
            page_title = page_title_search[0] # Take the first search result
            
            # Store the page object in self.page for other methods to use
            self.page = wikipedia.page(page_title, auto_suggest=False) 

        except wikipedia.exceptions.DisambiguationError as e:
            print(f"Topic '{topic}' is ambiguous. Options: {e.options[:5]}")
            if e.options:
                try:
                    # Try to use the first disambiguation option
                    self.page = wikipedia.page(e.options[0], auto_suggest=False)
                except Exception as inner_e:
                    print(f"Could not fetch disambiguated page: {inner_e}")
                    return []
            else:
                return []
        except wikipedia.exceptions.PageError:
            # page_title might not be defined if wikipedia.search failed and page_title_search was empty.
            resolved_page_title = page_title if 'page_title' in locals() and page_title else topic
            print(f"Page for '{topic}' (resolved to '{resolved_page_title}') does not exist.")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

        # Ensure self.page is set before proceeding
        if not self.page:
            print(f"Failed to load Wikipedia page for topic: {topic}")
            return []

        # Step 2: Apply different strategies to extract information
        if 'summary' in strategies:
            cards_from_summary = self._extract_from_summary(self.page.summary, num_cards_desired // len(strategies))
            flashcards.extend(cards_from_summary)

        if 'infobox' in strategies and hasattr(self.page, 'infobox') and self.page.infobox:
             # Placeholder for infobox parsing
             pass # print(f"Infobox found for {self.page.title}, needs parsing strategy.")

        if 'headings_detailed' in strategies:
            cards_from_headings = self._extract_from_sections_content(self.page, num_cards_desired // len(strategies))
            flashcards.extend(cards_from_headings)
        
        # Step 3: Filter, refine, and limit the number of cards
        flashcards = self._refine_flashcards(flashcards, num_cards_desired)
        
        return flashcards

    def _extract_from_summary(self, summary_text: str, max_cards: int):
        cards = []
        sentences = summary_text.split('. ') 
        page_title_for_question = self.page.title if self.page else "Topic"
        definition_indicators = [" is ", " are ", " was ", " were "]

        for sentence in sentences:
            if len(cards) >= max_cards:
                break
            
            sentence_stripped = sentence.strip()
            if not sentence_stripped: # Skip empty or whitespace-only sentences
                continue

            found_indicator = False
            for indicator in definition_indicators:
                if indicator in sentence_stripped.lower():
                    parts = sentence_stripped.split(indicator, 1)
                    front_candidate = parts[0].strip()
                    back_candidate = parts[1].strip()

                    # Avoid creating questions for very short subjects or pronouns alone if possible
                    # and ensure back has substance
                    if front_candidate and len(front_candidate) < 100 and len(back_candidate) > 10:
                        front = f"What {indicator.strip()} {front_candidate}?"
                        
                        # Ensure the 'back' ends with a period if it doesn't have other terminal punctuation.
                        if back_candidate and not back_candidate.endswith(('.', '!', '?')):
                            back_candidate += "."
                        
                        cards.append({"front": front, "back": back_candidate})
                        found_indicator = True
                        break # Found an indicator for this sentence, move to the next sentence
            
            if len(cards) >= max_cards: # Check again in case the last card filled max_cards
                break

        # If after iterating through sentences, no cards were made from definitions,
        # and there was at least one sentence, try the original fallback on the first sentence.
        if not cards and sentences and sentences[0].strip():
            first_sentence_content = sentences[0].strip()
            if len(first_sentence_content) > 30: # Original condition for fallback
                back_content = first_sentence_content
                if not back_content.endswith(('.', '!', '?')):
                    back_content += "."
                cards.append({"front": f"Summarize: {page_title_for_question}", "back": back_content})
        
        return cards[:max_cards]

    def _extract_from_sections_content(self, page_object, max_cards_total: int):
        cards = []
        sections = page_object.sections
        num_sections_to_process = min(len(sections), max_cards_total + 5)

        for section_title in sections[:num_sections_to_process]:
            if not section_title.lower() in ["see also", "references", "external links", "notes"]:
                try:
                    section_content = page_object.section(section_title)
                    if section_content and len(section_content.strip()) > 50:
                        paragraphs = section_content.split('\n\n')
                        first_paragraph = paragraphs[0].strip()
                        sentences = first_paragraph.split('. ')
                        answer_content = ". ".join(sentences[:2]) + ("." if sentences and sentences[0] and not sentences[0].endswith(".") else "")
                        if len(answer_content) > 30:
                            cards.append({"front": f"What about '{section_title}' in {page_object.title}?", "back": answer_content})
                except Exception as e:
                    print(f"Error processing section '{section_title}': {e}")
            if len(cards) >= max_cards_total:
                break
        return cards

    def _refine_flashcards(self, cards: list, num_desired: int):
        unique_cards = []
        seen_fronts = set()
        for card in cards:
            if card['front'] not in seen_fronts:
                if len(card['front']) > 10 and len(card['back']) > 20 and len(card['front']) < 200 and len(card['back']) < 500:
                    unique_cards.append(card)
                    seen_fronts.add(card['front'])
        return unique_cards[:num_desired]
