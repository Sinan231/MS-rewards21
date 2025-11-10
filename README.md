# Bing Search Automation

Automated system that fetches 10 top trending Google searches + 90 random web searches and executes them through your Bing account every 13-15 hours using browser automation.

## Features

- 🔍 **Mixed Search Strategy**: 10 trending Google searches + 90 realistic random web searches
- 🤖 **Browser Automation**: Uses Selenium with Microsoft Edge for realistic search behavior
- 👥 **Multi-Account Support**: Automatic detection and selection of Edge browser profiles
- ⏰ **Manual Control**: You decide when to run each batch (tracks timing)
- 📊 **Progress Tracking**: Real-time progress display and detailed logging
- 🎯 **Human-like Behavior**: Random delays between searches (2-5 seconds)
- 📝 **Complete Logging**: Search history and error tracking
- 🎲 **Realistic Random Searches**: Generates diverse, natural-looking search queries
- 💾 **Profile Memory**: Remembers your selected Edge profile for future runs

## Prerequisites

1. **Python 3.8+** installed
2. **Microsoft Edge browser** installed
3. **Multiple Edge profiles** (if you have multiple Microsoft accounts)
4. **Users logged into their respective Microsoft/Bing accounts** in Edge profiles
5. **SerpApi account** (free tier available)

### Edge Profile Setup

To use multiple accounts, create separate Edge profiles:
1. Open Edge browser
2. Click profile icon (top right) → "Add profile"
3. Sign into each Microsoft account in its own profile
4. Name profiles clearly (e.g., "Personal", "Work", "Gaming")

## Quick Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your SerpApi key
# Get your key from: https://serpapi.com/
```

Edit `.env` file:
```
SERPAPI_KEY=your_actual_serpapi_key_here
```

### 3. First Run

```bash
python main.py
```

## Usage

### Check Status
```bash
python main.py
```
Shows last execution time and hours since last run.

### Run Search Batch
```bash
# Interactive mode (shows status, asks for confirmation)
python main.py

# Direct execution (no prompts)
python main.py --run

# Custom number of searches
python main.py --limit 50

# Status only
python main.py --status
```

### Test System
```bash
python main.py --test
```
Tests API key and browser connection.

## Command Line Options

| Option | Description |
|--------|-------------|
| `--run` | Run search batch without prompting |
| `--status` | Show only status information |
| `--limit N` | Number of searches to perform (default: 100 total) |
| `--test` | Test browser and API connection |

## How It Works

1. **Fetch Trending Searches**: Gets top 10 trending searches from Google Trends API
2. **Generate Random Searches**: Creates 90 realistic random search queries using templates and word banks
3. **Mix & Shuffle**: Combines and randomizes the order of all searches
4. **Browser Setup**: Opens Edge using your existing profile (stays logged in)
5. **Execute Searches**: Performs each search with realistic delays
6. **Track Progress**: Shows real-time progress (1/100, 2/100, etc.)
7. **Log Results**: Records all searches and outcomes

## File Structure

```
.
├── main.py                 # Main execution controller
├── google_trends.py        # Google Trends API integration
├── random_searches.py      # Random search query generator
├── bing_automator.py       # Bing search automation
├── config.py              # Configuration management
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your API key (create this)
├── last_run.txt           # Timestamp of last execution
├── logs/
│   ├── search_history.log  # All executed searches
│   └── errors.log         # Error logs
└── README.md              # This file
```

## Example Output

```
==================================================
Bing Search Automation Status
==================================================
Current time: 2024-01-15 10:30:45
Last execution: 2024-01-14 21:15:30 (13h 15m ago)
Hours since last run: 13.3
✓ Ready for next execution (13+ hours elapsed)
==================================================

🚀 Starting Bing search automation with 100 searches...
This will fetch trending searches + random web searches
Please ensure your Edge browser is logged into your Microsoft account

Continue? (y/n): y

📡 Validating SerpApi key...
✅ API key valid
🌐 Testing browser connection...
✅ Browser connection successful
📊 Fetching 10 trending + 90 random searches...
✅ Successfully prepared 100 search terms
Sample searches: latest election news, how to learn python, weather forecast new york...

🔍 Starting Bing search automation...
[  1/100] ✓ latest news today
[  2/100] ✓ weather forecast
[  3/100] ✓ breaking news
...
[100/100] ✓ celebrity news

📈 Search batch completed!
✅ Successful searches: 98
❌ Failed searches: 2
📊 Success rate: 98.0%
⏰ Last run time updated: 2024-01-15 10:35:12
```

## Browser Requirements

- **Microsoft Edge** must be installed
- **User must be logged into Microsoft/Bing account** in Edge
- The automation uses your existing browser profile to maintain login state
- Browser will open/close automatically during execution

## Timing Recommendations

- **Recommended interval**: 13-15 hours between batches
- **Script tracks timing**: Shows hours since last execution
- **Manual control**: You decide when to run each batch
- **Duration**: ~3-5 minutes for 100 searches (10 trending + 90 random)

## Troubleshooting

### Common Issues

**"Invalid SerpApi key"**
- Check your .env file contains correct API key
- Get a key from https://serpapi.com/

**"Browser connection failed"**
- Ensure Microsoft Edge is installed
- Make sure you're logged into Bing in Edge
- Try running `python main.py --test`

**"Search box not found"**
- Bing may have updated their page layout
- Check internet connection
- Try running again after a few minutes

### Log Files

- `logs/search_history.log`: All executed searches with timestamps
- `logs/errors.log`: Detailed error information

### Error Recovery

- **Network issues**: Script retries with exponential backoff
- **Browser crashes**: Auto-restarts and continues
- **API failures**: Retries up to 3 times with delays

## Security & Privacy

- **API Key**: Stored in .env file (never in code)
- **Browser Privacy**: Uses your existing profile (not incognito)
- **Search Data**: Only logs search terms and timestamps
- **No Personal Data**: Never stores search results or personal information

## Configuration

### Modify Settings

Edit `config.py` to adjust:
- `DEFAULT_SEARCH_LIMIT`: Total number of searches (default: 100)
- `TRENDING_SEARCHES_COUNT`: Number of trending searches (default: 10)
- `RANDOM_SEARCHES_COUNT`: Number of random searches (default: 90)
- `HUMAN_DELAY_MIN/MAX`: Random delay range (default: 2-5 seconds)
- `BING_URL`: Bing search URL
- Log file locations

### Environment Variables

```bash
# Required
SERPAPI_KEY=your_serpapi_key

# Optional (overrides config.py values)
DEFAULT_SEARCH_LIMIT=50
TRENDING_SEARCHES_COUNT=5
RANDOM_SEARCHES_COUNT=45
HUMAN_DELAY_MIN=3
HUMAN_DELAY_MAX=7
```

## API Limits

- **SerpApi**: Free tier includes 100 searches/month
- **Google Trends**: Rate limited by SerpApi
- **Bing**: No official limits for normal usage

## Support

For issues or questions:
1. Check logs in `logs/` directory
2. Run `python main.py --test` for diagnostics
3. Ensure all prerequisites are met

## License

This project is for educational and personal use only. Please respect the terms of service of all involved services.