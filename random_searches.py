import random
import time
import logging
from datetime import datetime
import requests
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

# Templates for generating realistic random searches
SEARCH_TEMPLATES = [
    # News and current events
    "{adjective} {noun} news today",
    "latest {noun} updates",
    "breaking {noun} right now",
    "what is happening with {noun}",
    "{noun} developments this week",

    # Information seeking
    "how to {verb} {noun}",
    "best {noun} for {purpose}",
    "{noun} vs {alternative} comparison",
    "what is {concept} definition",
    "{noun} tutorial guide",

    # Entertainment and media
    "watch {media_type} online free",
    "new {media_type} releases 2024",
    "popular {media_type} this month",
    "{celebrity} latest news",
    "best {entertainment} recommendations",

    # Shopping and products
    "buy {product} online",
    "cheap {product} deals",
    "review of {product_name}",
    "best {product_category} 2024",
    "{product} discount codes",

    # Health and lifestyle
    "healthy {food_item} recipes",
    "exercise for {fitness_goal}",
    "mental health tips for {situation}",
    "benefits of {activity}",
    "how to improve {skill}",

    # Technology and science
    "new {technology} trends",
    "{software} vs {alternative}",
    "best {tech_category} tools",
    "how does {technology} work",
    "latest {science_topic} discoveries",

    # Travel and places
    "best places to visit in {location}",
    "cheap flights to {destination}",
    "hotels in {city} reviews",
    "things to do in {location}",
    "travel tips for {destination}",

    # Weather and environment
    "weather forecast for {location}",
    "climate change effects on {region}",
    "natural disasters in {area}",
    "best time to visit {location}",
    "seasonal weather patterns",
]

# Word banks for generating searches
ADJECTIVES = [
    "latest", "breaking", "new", "recent", "top", "best", "popular", "trending",
    "important", "significant", "major", "urgent", "critical", "viral", "hot"
]

NOUNS = [
    "politics", "economy", "technology", "science", "health", "sports", "entertainment",
    "business", "finance", "education", "climate", "weather", "markets", "stocks",
    "crypto", "ai", "gadgets", "software", "movies", "music", "games", "fashion"
]

VERBS = [
    "learn", "find", "search", "discover", "explore", "understand", "master", "create",
    "build", "develop", "improve", "fix", "solve", "buy", "sell", "trade", "invest"
]

PURPOSES = [
    "beginners", "experts", "students", "professionals", "home", "business", "personal",
    "online", "offline", "free", "premium", "cheap", "quality", "fast", "easy"
]

MEDIA_TYPES = [
    "movies", "tv shows", "music", "videos", "podcasts", "games", "books", "articles"
]

CELEBRITIES = [
    "Taylor Swift", "Elon Musk", "Beyonce", "Chris Rock", "Kevin Hart", "Dwayne Johnson",
    "Tom Cruise", "Leonardo DiCaprio", "Jennifer Lopez", "Brad Pitt", "Will Smith"
]

PRODUCTS = [
    "iPhone", "laptop", "headphones", "smartwatch", "tablet", "camera", "shoes", "clothing",
    "makeup", "skincare", "fitness tracker", "gaming console", "TV", "speaker"
]

PRODUCT_CATEGORIES = [
    "smartphones", "laptops", "headphones", "smartwatches", "tablets", "cameras",
    "shoes", "clothing", "makeup", "skincare", "fitness", "gaming", "electronics"
]

TECHNOLOGIES = [
    "artificial intelligence", "machine learning", "blockchain", "cryptocurrency",
    "cloud computing", "5G", "IoT", "virtual reality", "augmented reality", "quantum"
]

LOCATIONS = [
    "New York", "London", "Paris", "Tokyo", "Sydney", "Dubai", "Singapore", "Hong Kong",
    "Los Angeles", "Chicago", "Toronto", "Mumbai", "Berlin", "Rome", "Barcelona"
]

destinations = [
    "Europe", "Asia", "America", "Africa", "Australia", "Caribbean", "Hawaii", "Alaska",
    "Mexico", "Canada", "Thailand", "Japan", "Italy", "France", "Spain", "Greece"
]

def get_trending_keywords():
    """
    Get a list of current trending keywords to make searches more realistic.

    Returns:
        list: List of trending keywords
    """
    trending_keywords = [
        # Timeless popular topics
        "weather", "news", "stocks", "crypto", "ai", "election", "economy", "inflation",
        "jobs", "salary", "remote work", "vaccine", "climate", "energy", "gas prices",
        "housing", "mortgage", "interest rates", "social security", "healthcare",

        # Seasonal topics (adjust these based on current time)
        "hurricane season", "summer travel", "back to school", "holiday shopping",
        "tax deadline", "olympics", "world cup", "super bowl", "graduation",

        # Evergreen interests
        "weight loss", "diet", "exercise", "meditation", "sleep", "stress relief",
        "productivity", "time management", "career change", "retirement planning",

        # Tech topics
        "chatgpt", "smart home", "electric cars", "renewable energy", "space exploration",
        "cybersecurity", "data privacy", "social media", "streaming services"
    ]

    return trending_keywords

def generate_random_search():
    """
    Generate a single realistic random search query.

    Returns:
        str: Random search query
    """
    # Mix of different generation strategies
    strategy = random.choice(['template', 'keyword', 'question', 'local'])

    if strategy == 'template':
        # Use templates with random word banks
        template = random.choice(SEARCH_TEMPLATES)
        return template.format(
            adjective=random.choice(ADJECTIVES),
            noun=random.choice(NOUNS),
            verb=random.choice(VERBS),
            purpose=random.choice(PURPOSES),
            media_type=random.choice(MEDIA_TYPES),
            celebrity=random.choice(CELEBRITIES),
            entertainment=random.choice(['movies', 'music', 'shows', 'games']),
            product=random.choice(PRODUCTS),
            product_name=random.choice(PRODUCTS),
            product_category=random.choice(PRODUCT_CATEGORIES),
            alternative=random.choice(['competitors', 'alternatives', 'options']),
            concept=random.choice(NOUNS),
            fitness_goal=random.choice(['weight loss', 'muscle gain', 'endurance']),
            situation=random.choice(['stress', 'anxiety', 'work', 'school']),
            skill=random.choice(['coding', 'writing', 'speaking', 'leadership']),
            technology=random.choice(TECHNOLOGIES),
            tech_category=random.choice(['software', 'hardware', 'apps', 'tools']),
            science_topic=random.choice(['space', 'medicine', 'environment', 'physics']),
            location=random.choice(LOCATIONS),
            destination=random.choice(destinations),
            city=random.choice(LOCATIONS),
            area=random.choice(['region', 'zone', 'district']),
            region=random.choice(['northeast', 'southwest', 'midwest', 'west coast'])
        )

    elif strategy == 'keyword':
        # Combine trending keywords
        trending = get_trending_keywords()
        keywords = random.sample(trending, min(random.randint(1, 3), len(trending)))
        return ' '.join(keywords)

    elif strategy == 'question':
        # Generate question-based searches
        questions = [
            "what is {topic}",
            "how to {action}",
            "why is {phenomenon}",
            "where to find {item}",
            "when does {event}",
            "who won {competition}",
            "which {product} is best",
            "can you {possibility}",
            "should I {decision}",
            "are there {availability}"
        ]

        topics = get_trending_keywords() + NOUNS + [
            "bitcoin price", "gas prices", "stock market", "unemployment rate",
            "mortgage rates", "inflation data", "job openings", "housing market"
        ]

        actions = VERBS + [
            "save money", "invest", "lose weight", "learn coding", "start business",
            "buy house", "find job", "improve credit", "retire early", "travel cheap"
        ]

        return random.choice(questions).format(
            topic=random.choice(topics),
            action=random.choice(actions),
            phenomenon=random.choice(['climate change', 'inflation rising', 'market crashing']),
            item=random.choice(['deals', 'jobs', 'housing', 'information']),
            event=random.choice(['election', 'olympics', 'world cup', 'super bowl']),
            competition=random.choice(['election', 'championship', 'award', 'lottery']),
            product=random.choice(PRODUCT_CATEGORIES),
            possibility=random.choice(['work from home', 'invest in crypto', 'retire early']),
            decision=random.choice(['buy now', 'wait', 'invest', 'sell']),
            availability=random.choice(['jobs available', 'housing options', 'deals today'])
        )

    else:  # strategy == 'local'
        # Location-based searches
        locations = LOCATIONS + [
            "near me", "downtown", "suburbs", "city center", "airport",
            "mall", "hospital", "school", "park", "beach"
        ]

        local_searches = [
            "restaurants near {location}",
            "gas prices in {location}",
            "weather {location}",
            "jobs in {location}",
            "real estate {location}",
            "events {location} this weekend",
            "hotels {location}",
            "things to do {location}",
            "news {location}",
            "traffic {location}"
        ]

        return random.choice(local_searches).format(
            location=random.choice(locations)
        )

def get_random_searches(count=None):
    """
    Generate a list of random search queries.

    Args:
        count (int): Number of searches to generate (default: RANDOM_SEARCHES_COUNT)

    Returns:
        list: List of random search strings
    """
    if count is None:
        count = Config.RANDOM_SEARCHES_COUNT

    logging.info(f"Generating {count} random search queries")

    searches = []
    seen_searches = set()

    while len(searches) < count:
        search = generate_random_search()

        # Avoid duplicates
        if search not in seen_searches:
            searches.append(search)
            seen_searches.add(search)
        else:
            # If we get too many duplicates, just break to avoid infinite loop
            if len(seen_searches) < count * 0.1:  # Less than 10% unique
                break

    logging.info(f"Generated {len(searches)} unique random searches")
    return searches[:count]

def get_mixed_searches(trending_count=None, random_count=None):
    """
    Get a mix of trending and random searches.

    Args:
        trending_count (int): Number of trending searches
        random_count (int): Number of random searches

    Returns:
        list: Combined list of search terms
    """
    from google_trends import get_trending_searches

    if trending_count is None:
        trending_count = Config.TRENDING_SEARCHES_COUNT
    if random_count is None:
        random_count = Config.RANDOM_SEARCHES_COUNT

    try:
        trending = get_trending_searches(limit=trending_count)
        logging.info(f"Retrieved {len(trending)} trending searches")
    except Exception as e:
        logging.error(f"Failed to get trending searches: {e}")
        trending = []

    random_searches = get_random_searches(count=random_count)

    # Combine and mix them together
    all_searches = trending + random_searches
    random.shuffle(all_searches)  # Randomize the order

    logging.info(f"Created mixed search list: {len(trending)} trending + {len(random_searches)} random = {len(all_searches)} total")

    return all_searches