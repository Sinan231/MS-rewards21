import time
import logging
from serpapi import GoogleSearch
from config import Config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(Config.ERROR_LOG_FILE),
        logging.StreamHandler()
    ]
)

def get_trending_searches(api_key=None, limit=100, max_retries=3):
    """
    Fetch trending search terms from Google Trends API.

    Args:
        api_key (str): SerpApi API key
        limit (int): Number of search terms to fetch (max 100)
        max_retries (int): Maximum number of retry attempts

    Returns:
        list: List of search term strings
    """
    if not api_key:
        api_key = Config.SERPAPI_KEY
        if not api_key:
            raise ValueError("SerpApi key is required. Set SERPAPI_KEY environment variable.")

    if limit > 100:
        limit = 100

    params = {
        "engine": "google_trends_trending_now",
        "geo": "US",
        "no_cache": "true",
        "api_key": api_key
    }

    retry_count = 0
    backoff_delay = 1

    while retry_count < max_retries:
        try:
            logging.info(f"Fetching trending searches from Google Trends (attempt {retry_count + 1}/{max_retries})")
            search = GoogleSearch(params)
            results = search.get_dict()

            # Check for API errors
            if "error" in results:
                raise Exception(f"SerpApi error: {results['error']}")

            # Extract search terms from trending_searches
            search_terms = []
            trending_searches = results.get("trending_searches", [])

            if not trending_searches:
                logging.warning("No trending searches found in API response")
                return []

            for item in trending_searches[:limit]:
                if "query" in item:
                    search_terms.append(item["query"])

            logging.info(f"Successfully fetched {len(search_terms)} trending searches")
            return search_terms

        except Exception as e:
            retry_count += 1
            error_msg = f"Error fetching trending searches (attempt {retry_count}/{max_retries}): {str(e)}"
            logging.error(error_msg)

            if retry_count >= max_retries:
                logging.error("Max retries exceeded. Failed to fetch trending searches.")
                raise Exception(error_msg)

            # Exponential backoff
            logging.info(f"Waiting {backoff_delay}s before retry...")
            time.sleep(backoff_delay)
            backoff_delay *= 2

    return []

def validate_api_key(api_key):
    """
    Validate the SerpApi key by making a small test request.

    Args:
        api_key (str): SerpApi API key to validate

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        params = {
            "engine": "google_trends_trending_now",
            "geo": "US",
            "no_cache": "true",
            "api_key": api_key
        }

        search = GoogleSearch(params)
        results = search.get_dict()

        # If we get results without an error, key is valid
        return "error" not in results

    except Exception as e:
        logging.error(f"API key validation failed: {str(e)}")
        return False