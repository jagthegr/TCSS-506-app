# llm_flashcard_generator.py
import google.generativeai as genai
import json
import logging
# Assuming you have llm_config.py in the same directory or yourPYTHONPATH is set
from .llm_agent import load_api_key, DEFAULT_LLM_MODEL # REVERTED IMPORT

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load API Key and configure Gemini
try:
    GOOGLE_API_KEY = load_api_key() # REVERTED USAGE
    genai.configure(api_key=GOOGLE_API_KEY)
    logging.info("Google Generative AI configured successfully.")
except ValueError as e:
    logging.error(f"Fatal error during LLM configuration: {e}")
    # Depending on your app structure, you might want to exit or handle this more gracefully
    raise
except Exception as e:
    logging.error(f"An unexpected error occurred during LLM configuration: {e}")
    raise

# Initialize the Generative Model (you can make this more dynamic if needed)
# Basic generation config for JSON output
generation_config = {
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192, # Gemini 1.5 Flash can handle large outputs
    "response_mime_type": "application/json",
}

# Basic safety settings - adjust as needed
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

try:
    llm_model = genai.GenerativeModel(
        model_name=DEFAULT_LLM_MODEL, # REVERTED USAGE
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    logging.info(f"LLM Model '{DEFAULT_LLM_MODEL}' initialized.")
except Exception as e:
    logging.error(f"Error initializing LLM model '{DEFAULT_LLM_MODEL}': {e}")
    raise

def generate_llm_flashcards(input_text_or_topic: str, num_flashcards: int = 5):
    """
    Generates flashcards using the LLM based on the input text or topic.

    Args:
        input_text_or_topic (str): The text or topic to generate flashcards from.
        num_flashcards (int): The number of flashcards to generate. Defaults to 5.

    Returns:
        list: A list of flashcard dictionaries (e.g., [{"front": "Q1", "back": "A1"}, ...])
              or an empty list if generation fails or validation is unsuccessful.
    """
    logging.info(f"Attempting to generate {num_flashcards} flashcards for: '{input_text_or_topic[:50]}...'")

    prompt_text = f"""
Please generate {num_flashcards} flashcards based on the following text or topic:
'{input_text_or_topic}'

Each flashcard must be a JSON object with a "front" key (for the question or term)
and a "back" key (for the answer or definition).
The overall output must be a JSON list of these flashcard objects.

For example:
[
  {{"front": "What is the capital of France?", "back": "Paris."}},
  {{"front": "What is 2 + 2?", "back": "4."}}
]

Generate exactly {num_flashcards} flashcards.
"""

    try:
        logging.debug(f"Sending prompt to LLM: {prompt_text}")
        response = llm_model.generate_content(prompt_text)

        # Log any prompt feedback
        if response.prompt_feedback:
            logging.warning(f"LLM prompt feedback: {response.prompt_feedback}")
            if response.prompt_feedback.block_reason:
                logging.error(f"Content generation blocked. Reason: {response.prompt_feedback.block_reason_message or response.prompt_feedback.block_reason}")
                return []

        if not hasattr(response, 'text') or not response.text:
            logging.error("LLM response is empty or does not have a 'text' attribute.")
            return []

        llm_output_text = response.text
        logging.info("LLM response received successfully.")
        logging.debug(f"Raw LLM output: {llm_output_text[:200]}...") # Log a snippet

    except Exception as e:
        logging.error(f"Error during LLM API call: {e}")
        return []

    try:
        logging.info("Attempting to parse LLM response as JSON.")
        flashcards_data = json.loads(llm_output_text)
        logging.info("LLM response parsed as JSON successfully.")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode LLM response as JSON: {e}")
        logging.error(f"LLM output that failed to parse: {llm_output_text}")
        return []
    except Exception as e:
        logging.error(f"An unexpected error occurred during JSON parsing: {e}")
        return []

    # Validate the structure of the parsed JSON
    if not isinstance(flashcards_data, list):
        logging.error(f"Parsed JSON is not a list. Received type: {type(flashcards_data)}")
        return []

    validated_flashcards = []
    for i, item in enumerate(flashcards_data):
        if not isinstance(item, dict):
            logging.warning(f"Item at index {i} in JSON list is not a dictionary. Type: {type(item)}. Skipping.")
            continue
        if "front" not in item or not isinstance(item["front"], str):
            logging.warning(f"Flashcard at index {i} missing 'front' key or 'front' is not a string. Item: {item}. Skipping.")
            continue
        if "back" not in item or not isinstance(item["back"], str):
            logging.warning(f"Flashcard at index {i} missing 'back' key or 'back' is not a string. Item: {item}. Skipping.")
            continue
        validated_flashcards.append({"front": item["front"], "back": item["back"]})

    if not validated_flashcards:
        logging.warning("No valid flashcards found after validation, or initial list was empty.")
        return []
    
    if len(validated_flashcards) != len(flashcards_data):
        logging.warning(f"Some flashcards were filtered out during validation. Original: {len(flashcards_data)}, Validated: {len(validated_flashcards)}")


    logging.info(f"Successfully generated and validated {len(validated_flashcards)} flashcards.")
    return validated_flashcards

# Example usage (optional, for testing this script directly)
if __name__ == "__main__":
    logging.info("Starting LLM Flashcard Generator direct test...")
    try:
        # Test case 1: Simple topic
        topic1 = "Basic Python Data Types"
        print(f"\\n--- Generating flashcards for: {topic1} ---")
        flashcards1 = generate_llm_flashcards(topic1, num_flashcards=3)
        if flashcards1:
            print("Generated Flashcards:")
            for card in flashcards1:
                print(f"  Front: {card['front']}")
                print(f"  Back: {card['back']}")
        else:
            print("No flashcards generated or validation failed.")

        # Test case 2: More complex input text
        text2 = """Photosynthesis is a process used by plants, algae, and certain bacteria to
        harness energy from sunlight and turn it into chemical energy. The process typically
        involves the green pigment chlorophyll and generates oxygen as a byproduct."""
        print(f"\\n--- Generating flashcards for: Photosynthesis (text input) ---")
        flashcards2 = generate_llm_flashcards(text2, num_flashcards=2)
        if flashcards2:
            print("Generated Flashcards:")
            for card in flashcards2:
                print(f"  Front: {card['front']}")
                print(f"  Back: {card['back']}")
        else:
            print("No flashcards generated or validation failed.")
        
        # Test case 3: Requesting zero flashcards (should ideally be handled by prompt or return empty)
        # Depending on LLM, it might still generate something or error.
        # The current prompt asks for 'num_flashcards', so 0 might be odd.
        # Let's test with 1 to see if it respects the count.
        topic3 = "The concept of a variable in programming"
        print(f"\\n--- Generating flashcards for: {topic3} (requesting 1) ---")
        flashcards3 = generate_llm_flashcards(topic3, num_flashcards=1)
        if flashcards3:
            print("Generated Flashcards:")
            for card in flashcards3:
                print(f"  Front: {card['front']}")
                print(f"  Back: {card['back']}")
        else:
            print("No flashcards generated or validation failed.")

    except Exception as e:
        logging.error(f"Error in __main__ test execution: {e}")
        print(f"An error occurred during the test: {e}")
    finally:
        logging.info("LLM Flashcard Generator direct test finished.")