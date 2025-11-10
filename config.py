import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    DEFAULT_SEARCH_LIMIT = 100
    TRENDING_SEARCHES_COUNT = 10  # Top trending searches
    RANDOM_SEARCHES_COUNT = 90    # Random web searches
    HUMAN_DELAY_MIN = 2.0  # seconds
    HUMAN_DELAY_MAX = 5.0  # seconds
    BING_URL = "https://bing.com"
    LOG_FILE = "logs/search_history.log"
    ERROR_LOG_FILE = "logs/errors.log"
    LAST_RUN_FILE = "last_run.txt"