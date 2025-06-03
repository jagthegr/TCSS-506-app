# Python code to load environment variables using python-dotenv
# and specifically get 'GOOGLE_API_KEY'.
# Include a check to ensure the API key is loaded, raising an error if not.

# llm_config.py
import os
from dotenv import load_dotenv
import logging

# Determine the project root directory based on the location of this file
# This assumes llm_agent.py is in app/utils/
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOTENV_PATH = os.path.join(PROJECT_ROOT, '.env')

def load_api_key():
    """Loads the Google API key from a .env file in the project root."""
    # load_dotenv() # Original call
    load_dotenv(dotenv_path=DOTENV_PATH) # Explicit path
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        logging.error(f"GOOGLE_API_KEY not found in .env file (expected at {DOTENV_PATH}) or environment variables.")
        raise ValueError(f"GOOGLE_API_KEY is not set. Please check {DOTENV_PATH}.")
    return api_key

# You can add other configurations here if needed later
# For example, default LLM model name
DEFAULT_LLM_MODEL = "gemini-1.5-flash-latest"

if __name__ == "__main__":
    try:
        print("Attempting to load API key directly in llm_agent.py...")
        key = load_api_key()
        print("SUCCESS: Google API Key loaded (first 5 chars):", key[:5] + "...")
        print("SUCCESS: Default LLM Model:", DEFAULT_LLM_MODEL)
    except ValueError as e:
        print(f"ERROR in llm_agent.py direct test: {e}")
    except Exception as e:
        print(f"UNEXPECTED ERROR in llm_agent.py direct test: {e}")