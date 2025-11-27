# News Sentiment Analysis API

A Python API for analyzing stock/cryptocurrency news sentiment using AI-powered analysis with Google Gemini.

> **Note for Group Members:** When using this as a submodule, replace `from src import analyze_news` with `from llm_news_sentiment_analysis.src import analyze_news`.

## Features

- Fetches recent news articles for any ticker symbol (stocks, crypto, etc.)
- AI-powered sentiment analysis using Google Gemini
- Returns a sentiment score (0-100) with detailed reasoning
- Simple, clean API for easy integration

## Installation

### As a Git Submodule (Recommended for Group Projects)

1. Add this repository as a submodule in your group repo (use underscores, not dashes):
```bash
cd group-repo
git submodule add <repository-url> llm_news_sentiment_analysis
git submodule update --init --recursive
```
> **Important:** Use underscores (`_`) instead of dashes (`-`) in the submodule name because Python module names cannot contain dashes.

2. Install dependencies:
```bash
pip install -r llm_news_sentiment_analysis/requirements.txt
```

3. Set up your Google Gemini API key:
```bash
cd llm_news_sentiment_analysis
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Standalone Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Google Gemini API key:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

## API Usage

### Import Path

**If using as a submodule in your group repo:**
```python
from llm_news_sentiment_analysis.src import analyze_news
```

**If using standalone (within this project):**
```python
from src import analyze_news
```

### Basic Example

```python
# If this is a submodule named 'news_analysis' in your group repo:
from llm_news_sentiment_analysis.src import analyze_news

# Analyze news for a ticker
result = analyze_news("BTC-USD", num_articles=10)

print(f"Ticker: {result['ticker']}")
print(f"Score: {result['score']}/100")
print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']}")
print(f"Reason: {result['reason']}")
```

### Function Signature

```python
analyze_news(ticker, num_articles=10, verbose=False)
```

**Parameters:**
- `ticker` (str): Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'BTC-USD')
- `num_articles` (int, optional): Number of articles to fetch and analyze (default: 10)
- `verbose` (bool, optional): If True, prints progress messages (default: False)

**Returns:**
- `dict`: Analysis score JSON with the following structure:
```python
{
    'ticker': 'BTC-USD',
    'score': 75,                           # 0-100 sentiment score
    'sentiment': 'Bullish',                # Sentiment label (Bullish/Bearish/Neutral)
    'confidence': 'High',                  # Confidence level (High/Medium/Low)
    'reason': 'Overall positive...'        # Detailed reasoning
}
```

## How It Works

1. **Fetch News**: Retrieves recent news articles for the specified ticker using yfinance
2. **Filter Important Articles**: Uses AI to identify which articles are most relevant
3. **Scrape Content**: Extracts full article text from important articles
4. **Sentiment Analysis**: Analyzes all articles and generates an overall sentiment score (0-100)
5. **Return Results**: Returns a clean JSON response with the score and reasoning

## Score Interpretation

The API returns both a numeric score (0-100) and a sentiment label:

**Sentiment Labels:**
- **Bullish**: Positive market outlook
- **Bearish**: Negative market outlook
- **Neutral**: Mixed or uncertain outlook

**Score Ranges:**
- **0-30**: Strong bearish sentiment
- **31-49**: Moderate bearish sentiment  
- **50**: Neutral sentiment
- **51-70**: Moderate bullish sentiment
- **71-100**: Strong bullish sentiment

**Confidence Levels:**
- **High**: Strong consensus in the news articles
- **Medium**: Moderate agreement across articles
- **Low**: Mixed or conflicting signals

## Requirements

- Python 3.7+
- yfinance
- google-generativeai
- requests
- beautifulsoup4

See `requirements.txt` for full dependencies.

## License

See LICENSE file for details.

## Notes

- Requires an active internet connection
- API calls are rate-limited by Google Gemini's free tier
- News availability depends on Yahoo Finance data
