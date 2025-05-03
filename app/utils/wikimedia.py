import requests

WIKIMEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

def search_wikimedia(query):
    """Searches Wikimedia Commons for a given query."""
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "utf8": 1,
        "formatversion": 2 # Use format version 2 for simpler JSON
    }
    try:
        response = requests.get(WIKIMEDIA_API_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        data = response.json()
        return data.get('query', {}).get('search', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Wikimedia API: {e}")
        return None
