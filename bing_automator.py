import time
import random
import logging
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import Config
from edge_profiles import get_profile_user_data_dir, get_profile_directory_name

# Set up logging for search history
search_logger = logging.getLogger('search_history')
search_logger.setLevel(logging.INFO)
search_handler = logging.FileHandler(Config.LOG_FILE)
search_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s'))
search_logger.addHandler(search_handler)

# Set up error logging
error_logger = logging.getLogger('errors')
error_logger.setLevel(logging.ERROR)
error_handler = logging.FileHandler(Config.ERROR_LOG_FILE)
error_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(funcName)s() | %(message)s'))
error_logger.addHandler(error_handler)

def setup_browser():
    """
    Set up and configure the Edge browser with existing user profile.

    Returns:
        webdriver.Edge: Configured Edge WebDriver instance
    """
    try:
        options = webdriver.EdgeOptions()

        # Use existing user data directory to stay logged in
        options.add_argument("--user-data-dir=default")
        options.add_argument("--profile-directory=Default")

        # Additional options for stability
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Auto-install and configure EdgeDriver
        service = Service(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

        # Set page load timeout
        driver.set_page_load_timeout(30)
        driver.maximize_window()

        logging.info("Browser setup completed successfully")
        return driver

    except Exception as e:
        error_logger.error(f"Failed to setup browser: {str(e)}")
        raise Exception(f"Browser setup failed: {str(e)}")

def human_delay():
    """
    Generate a random delay between searches to simulate human behavior.

    Returns:
        float: Delay duration in seconds
    """
    delay = random.uniform(Config.HUMAN_DELAY_MIN, Config.HUMAN_DELAY_MAX)
    time.sleep(delay)
    return delay

def search_bing(driver, search_term):
    """
    Execute a single search on Bing.

    Args:
        driver (webdriver.Edge): Selenium WebDriver instance
        search_term (str): Search term to execute

    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        # Navigate to Bing if not already there
        if "bing.com" not in driver.current_url:
            logging.info(f"Navigating to {Config.BING_URL}")
            driver.get(Config.BING_URL)
            time.sleep(2)

        # Find search box with multiple fallback strategies
        search_box = None
        search_selectors = [
            (By.ID, "sb_form_q"),           # Primary search box ID
            (By.NAME, "q"),                 # Name attribute fallback
            (By.CSS_SELECTOR, "input[type='search']"),  # Type attribute fallback
        ]

        for selector_type, selector_value in search_selectors:
            try:
                search_box = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((selector_type, selector_value))
                )
                break
            except:
                continue

        if not search_box:
            raise Exception("Search box not found with any selector")

        # Clear and enter search term
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)

        # Wait for search results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "b_results"))
        )

        # Log successful search
        search_logger.info(f'SUCCESS | "{search_term}"')
        return True, f"Successfully searched: {search_term}"

    except Exception as e:
        error_msg = f"Error searching '{search_term}': {str(e)}"
        error_logger.error(error_msg)
        search_logger.info(f'ERROR | "{search_term}" | {str(e)}')
        return False, error_msg

def execute_search_batch(search_terms):
    """
    Execute a batch of searches on Bing.

    Args:
        search_terms (list): List of search terms to execute

    Returns:
        list: List of result dictionaries with term, success, message, and timestamp
    """
    if not search_terms:
        logging.warning("No search terms provided")
        return []

    driver = None
    results = []
    successful_searches = 0
    failed_searches = 0

    try:
        logging.info(f"Starting search batch with {len(search_terms)} terms")
        driver = setup_browser()

        for i, term in enumerate(search_terms, 1):
            try:
                success, message = search_bing(driver, term)

                result = {
                    "term": term,
                    "success": success,
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                }
                results.append(result)

                if success:
                    successful_searches += 1
                else:
                    failed_searches += 1

                # Progress display
                status = "✓" if success else "✗"
                print(f"[{i:3d}/{len(search_terms)}] {status} {term}")

                # Human-like delay between searches (skip after last search)
                if i < len(search_terms):
                    delay = human_delay()

            except Exception as e:
                # Handle unexpected errors for individual searches
                error_msg = f"Unexpected error with search '{term}': {str(e)}"
                error_logger.error(error_msg)

                result = {
                    "term": term,
                    "success": False,
                    "message": error_msg,
                    "timestamp": datetime.now().isoformat()
                }
                results.append(result)
                failed_searches += 1

                status = "✗"
                print(f"[{i:3d}/{len(search_terms)}] {status} {term}")

                # Still add delay even on error
                if i < len(search_terms):
                    human_delay()

        # Log batch completion summary
        summary = f"Batch completed: {successful_searches} successful, {failed_searches} failed out of {len(search_terms)} total"
        logging.info(summary)
        print(f"\n{summary}")

    except Exception as e:
        error_logger.error(f"Critical error in search batch execution: {str(e)}")
        logging.error(f"Search batch failed: {str(e)}")

    finally:
        if driver:
            try:
                driver.quit()
                logging.info("Browser closed successfully")
            except Exception as e:
                error_logger.error(f"Error closing browser: {str(e)}")

    return results

def test_browser_connection():
    """
    Test if the browser can connect to Bing properly.

    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        driver = setup_browser()
        driver.get(Config.BING_URL)

        # Check if we can find the search box
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "sb_form_q"))
        )

        driver.quit()
        logging.info("Browser connection test successful")
        return True

    except Exception as e:
        error_logger.error(f"Browser connection test failed: {str(e)}")
        return False