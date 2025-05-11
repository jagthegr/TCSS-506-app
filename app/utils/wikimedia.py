import requests
from bs4 import BeautifulSoup
import re
from typing import Optional  # Added Optional for type hinting

from .wikipedia_agent import WikipediaFlashcardAgent  # Import the new agent

WIKIMEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

def search_wikimedia(query):
    """Searches Wikimedia Commons for a given query."""
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "utf8": 1,
        "formatversion": 2  # Use format version 2 for simpler JSON
    }
    try:
        response = requests.get(WIKIMEDIA_API_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        return data.get('query', {}).get('search', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Wikimedia API: {e}")
        return None

def get_wikipedia_page_html(page_title: str) -> Optional[str]:  # Changed to Optional[str]
    """Fetches the full HTML content of a Wikipedia page."""
    params = {
        "action": "parse",
        "page": page_title,
        "format": "json",
        "prop": "text",  # Requesting the parsed HTML content
        "formatversion": 2
    }
    try:
        response = requests.get(WIKIMEDIA_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if "parse" in data and "text" in data["parse"]:
            return data["parse"]["text"]
        else:
            print(f"Could not find text content for page: {page_title}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page HTML from Wikipedia API: {e}")
        return None

def clean_text(text: str) -> str:
    """Basic text cleaning: remove extra whitespace, newlines, and bracketed numbers like [1]."""
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
    text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with single space
    text = re.sub(r'\[\d+\]', '', text)  # Remove citation numbers like [1], [23]
    return text.strip()

def extract_flashcards_from_html_simple(html_content: str) -> list[tuple[str, str]]:
    """Extracts flashcards using section headings and first suitable paragraph (improved approach)."""
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    flashcards = []

    headings_found = soup.find_all(['h2', 'h3'])

    for i, heading in enumerate(headings_found):
        edit_span_in_heading = heading.find('span', class_='mw-editsection')
        if edit_span_in_heading:
            edit_span_in_heading.decompose()
        
        heading_text = heading.get_text(separator=' ', strip=True)
        heading_text = heading_text.replace("[edit]", "").replace("(edit)", "").strip()

        if not heading_text:
            continue

        answer_text = ""
        for element_count, next_elem in enumerate(heading.find_all_next()):
            if element_count > 50: 
                break

            if next_elem.name in ['h2', 'h3']:
                break 
            
            if next_elem.name == 'p':
                current_paragraph_text = next_elem.get_text(separator=' ', strip=True)

                if current_paragraph_text and len(current_paragraph_text) > 20:
                    answer_text = current_paragraph_text
                    break 
        
        if heading_text and answer_text:
            question = clean_text(heading_text)
            answer = clean_text(answer_text)
            
            if question and answer and len(question) > 3 and len(answer) > 20:
                flashcards.append((question, answer))

    return flashcards

def generate_flashcards_from_topic_agent(topic: str, num_cards_desired: int = 10) -> list[tuple[str, str]]:
    """
    Generates flashcards for a given topic using the WikipediaFlashcardAgent.
    """
    agent = WikipediaFlashcardAgent()
    # Call the agent with num_cards_desired
    agent_cards = agent.generate_flashcards(topic, num_cards_desired=num_cards_desired)
    
    # Convert agent's output (list of dicts) to list of tuples
    processed_cards = []
    for card_dict in agent_cards:
        if isinstance(card_dict, dict) and 'front' in card_dict and 'back' in card_dict:
            processed_cards.append((str(card_dict['front']), str(card_dict['back'])))
        else:
            # It's good to log or print if a card is malformed, 
            # helps in debugging the agent's output
            print(f"Warning: Skipping malformed card from agent: {card_dict}")
            
    return processed_cards
