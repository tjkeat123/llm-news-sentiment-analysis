import json
from .news import extract_news_fields, merge_important_info_from_json
from .xai import XAI

def analyze_news(ticker, num_articles=10, verbose=False):
    """
    Main API function: Fetch news articles for a ticker and analyze their sentiment.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., 'AAPL', 'TSLA', 'BTC-USD')
        num_articles (int): Number of articles to fetch and analyze (default: 10)
        verbose (bool): If True, print progress messages (default: False)
    
    Returns:
        dict: Analysis score JSON with structure:
            {
                'ticker': str,
                'score': int (0-100),
                'reason': str,
                'articles_analyzed': int,
                'important_articles': int
            }
    
    Example:
        >>> from src import analyze_news
        >>> result = analyze_news("AAPL", num_articles=10)
        >>> print(f"Score: {result['score']}/100")
    """
    if verbose:
        print(f"Fetching {num_articles} news articles for {ticker}...")
    
    # Step 1: Get news articles
    news_json = extract_news_fields(ticker, num_articles)
    
    # Step 2: Initialize XAI client
    llm = XAI()
    
    # Step 3: Analyze with XAI
    if verbose:
        print(f"Analyzing articles with XAI Grok...")
    response_json = llm.decide_news_importance(news_json)
    
    # Step 4: Merge news with importance decisions
    merged_json = merge_important_info_from_json(news_json, response_json)
    
    # Step 5: Get overall analysis score
    if verbose:
        print(f"Getting overall analysis score...")
    score_json = llm.get_analysis_score(merged_json)
    
    # Parse and return the score data
    score_data = json.loads(score_json)
    
    if verbose:
        print(f"Analysis complete: {score_data['score']}/100")
    
    return score_data

__all__ = ['analyze_news']

