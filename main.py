#!/usr/bin/env python3
import argparse
import os
import sys
from datetime import datetime, timedelta
from google_trends import get_trending_searches, validate_api_key
from random_searches import get_mixed_searches, get_random_searches
from bing_automator import execute_search_batch, test_browser_connection
from config import Config

def get_last_run_time():
    """
    Read the last execution timestamp from file.

    Returns:
        datetime or None: Last run time, or None if file doesn't exist
    """
    try:
        if os.path.exists(Config.LAST_RUN_FILE):
            with open(Config.LAST_RUN_FILE, 'r') as f:
                timestamp_str = f.read().strip()
                return datetime.fromisoformat(timestamp_str)
    except Exception as e:
        print(f"Warning: Could not read last run time: {e}")
    return None

def update_last_run_time():
    """
    Update the last execution timestamp file.
    """
    try:
        with open(Config.LAST_RUN_FILE, 'w') as f:
            f.write(datetime.now().isoformat())
    except Exception as e:
        print(f"Warning: Could not update last run time: {e}")

def format_time_ago(timestamp):
    """
    Convert timestamp to human-readable "X hours ago" format.

    Args:
        timestamp (datetime): Timestamp to format

    Returns:
        str: Human-readable time difference
    """
    if not timestamp:
        return "Never"

    now = datetime.now()
    diff = now - timestamp

    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        if minutes > 0:
            return f"{hours}h {minutes}m ago"
        else:
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"

def display_status():
    """
    Display the current status including last run time and hours since last execution.
    """
    last_run = get_last_run_time()
    current_time = datetime.now()

    print("=" * 50)
    print("Bing Search Automation Status")
    print("=" * 50)
    print(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

    if last_run:
        time_ago = format_time_ago(last_run)
        hours_since = (current_time - last_run).total_seconds() / 3600

        print(f"Last execution: {last_run.strftime('%Y-%m-%d %H:%M:%S')} ({time_ago})")
        print(f"Hours since last run: {hours_since:.1f}")

        if hours_since >= 13:
            print("✓ Ready for next execution (13+ hours elapsed)")
        else:
            remaining = 13 - hours_since
            print(f"⏰ Wait {remaining:.1f} more hours before next execution")
    else:
        print("Last execution: Never (first run)")

    print("=" * 50)

def run_search_batch(limit=None, skip_prompt=False, use_mixed_searches=True):
    """
    Execute the full search process: fetch trends, random searches, and perform Bing searches.

    Args:
        limit (int): Number of searches to perform (default from config)
        skip_prompt (bool): Skip user confirmation prompts
        use_mixed_searches (bool): Whether to use mixed trending+random or just trending
    """
    if limit is None:
        limit = Config.DEFAULT_SEARCH_LIMIT

    print(f"\n🚀 Starting Bing search automation with {limit} searches...")
    print("This will fetch trending searches + random web searches")
    print("Please ensure your Edge browser is logged into your Microsoft account\n")

    if not skip_prompt:
        confirm = input("Continue? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Search batch cancelled.")
            return False

    try:
        # Step 1: Validate API key
        print("📡 Validating SerpApi key...")
        if not validate_api_key(Config.SERPAPI_KEY):
            print("❌ Invalid SerpApi key. Please check your .env configuration.")
            return False
        print("✅ API key valid")

        # Step 2: Test browser connection
        print("🌐 Testing browser connection...")
        if not test_browser_connection():
            print("❌ Browser connection failed. Please ensure Edge browser is installed.")
            return False
        print("✅ Browser connection successful")

        # Step 3: Fetch search terms
        if use_mixed_searches:
            print(f"📊 Fetching {Config.TRENDING_SEARCHES_COUNT} trending + {Config.RANDOM_SEARCHES_COUNT} random searches...")
            search_terms = get_mixed_searches(
                trending_count=Config.TRENDING_SEARCHES_COUNT,
                random_count=Config.RANDOM_SEARCHES_COUNT
            )
        else:
            print(f"📊 Fetching top {limit} trending searches from Google...")
            search_terms = get_trending_searches(limit=limit)

        if not search_terms:
            print("❌ No searches found. Please check your internet connection.")
            return False

        # Limit to requested amount
        search_terms = search_terms[:limit]

        print(f"✅ Successfully prepared {len(search_terms)} search terms")
        print(f"Sample searches: {', '.join(search_terms[:3])}...\n")

        # Step 4: Execute searches
        print("🔍 Starting Bing search automation...")
        results = execute_search_batch(search_terms)

        # Step 5: Display results summary
        successful = sum(1 for r in results if r['success'])
        failed = len(results) - successful

        print(f"\n📈 Search batch completed!")
        print(f"✅ Successful searches: {successful}")
        print(f"❌ Failed searches: {failed}")
        print(f"📊 Success rate: {(successful/len(results)*100):.1f}%")

        if failed > 0:
            print(f"\n⚠️  {failed} searches failed. Check logs/errors.log for details.")

        # Step 6: Update last run time
        update_last_run_time()
        print(f"⏰ Last run time updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        return True

    except KeyboardInterrupt:
        print("\n\n⚠️  Search batch interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Search batch failed: {str(e)}")
        print("Please check logs/errors.log for detailed error information")
        return False

def main():
    """
    Main CLI interface for the Bing search automation tool.
    """
    parser = argparse.ArgumentParser(
        description="Automated Bing search using trending Google searches",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                 # Show status and prompt to run
  %(prog)s --run           # Run search batch without prompting
  %(prog)s --status        # Show only status
  %(prog)s --limit 10      # Run with 10 searches instead of default
  %(prog)s --test          # Test browser and API connection
        """
    )

    parser.add_argument('--run', action='store_true',
                       help='Run search batch without prompting')
    parser.add_argument('--status', action='store_true',
                       help='Show only status information')
    parser.add_argument('--limit', type=int, metavar='N',
                       help=f'Number of searches to perform (default: {Config.DEFAULT_SEARCH_LIMIT})')
    parser.add_argument('--test', action='store_true',
                       help='Test browser and API connection')

    args = parser.parse_args()

    # Check if configuration is properly set up
    if not Config.SERPAPI_KEY:
        print("❌ SerpApi key not configured!")
        print("Please set SERPAPI_KEY in your .env file")
        print("Create a .env file with your key from https://serpapi.com/")
        sys.exit(1)

    # Handle different command modes
    if args.test:
        print("🧪 Testing system configuration...")
        print("\n1. Testing API key...")
        if validate_api_key(Config.SERPAPI_KEY):
            print("✅ API key valid")
        else:
            print("❌ API key invalid")
            sys.exit(1)

        print("\n2. Testing browser connection...")
        if test_browser_connection():
            print("✅ Browser connection successful")
        else:
            print("❌ Browser connection failed")
            sys.exit(1)

        print("\n✅ All tests passed! System is ready to use.")
        return

    if args.status:
        display_status()
        return

    # Default behavior: show status and optionally run
    display_status()

    if args.run:
        success = run_search_batch(limit=args.limit, skip_prompt=True)
        sys.exit(0 if success else 1)
    else:
        # Show prompt for manual execution
        try:
            choice = input("\nRun search batch now? (y/n): ").strip().lower()
            if choice == 'y':
                success = run_search_batch(limit=args.limit, skip_prompt=False)
                sys.exit(0 if success else 1)
            else:
                print("Search batch cancelled.")
        except KeyboardInterrupt:
            print("\nGoodbye!")

if __name__ == "__main__":
    main()