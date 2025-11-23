import yfinance as yf
import json

def extract_news_fields(ticker, num_articles=10):
    """Extract specific fields from news articles and return as JSON string"""
    yf_ticker = yf.Ticker(ticker)
    news_list = yf_ticker.get_news(count=num_articles)
    
    result = {
        'ticker': ticker,
        'total_articles': 0,
        'articles': []
    }
    
    for idx, news in enumerate(news_list[:num_articles]):
        # the returned news is a dictionary with a key 'id' and 'content'
        content = news.get('content', {})
        
        # Get URL - prefer clickThroughUrl if available, otherwise canonicalUrl
        click_through = content.get('clickThroughUrl')
        canonical = content.get('canonicalUrl', {})
        
        # clickThroughUrl could be null, so check if it exists and has a url
        if click_through and click_through.get('url'):
            url = click_through.get('url')
        else:
            url = canonical.get('url')
        
        article_data = {
            'id': news.get('id'),
            'title': content.get('title'),
            'summary': content.get('summary'),
            'pubDate': content.get('pubDate'),
            'provider': content.get('provider', {}).get('displayName'),
            'url': url,
            'editorsPick': content.get('metadata', {}).get('editorsPick')
        }
        
        result['articles'].append(article_data)
    
    result['total_articles'] = len(result['articles'])
    
    # Return as JSON string
    return json.dumps(result, indent=2)