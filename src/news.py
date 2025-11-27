import yfinance as yf
import json

from .scraper import scrape_yfinance_article

def extract_news_fields(ticker, num_articles=10):
    """Extract specific fields from news articles and return as JSON string, if the article is not on Yahoo Finance, the url will be empty"""
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
        
        # Get URL - the url will be saved in clickThroughURL if the article is on Yahoo Finance,
        # otherwise the url will be save in canonicalURL (not implemented here)
        click_through = content.get('clickThroughUrl')
        
        # clickThroughUrl could be null, so check if it exists and has a url
        if click_through and click_through.get('url'):
            url = click_through.get('url')
        else:
            url = ""
        
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

def merge_important_info_from_json(news_json, importance_json):
    """Merge the news from the news JSON and the importance JSON"""
    news_data = json.loads(news_json)
    importance_data = json.loads(importance_json)

    merged_data = {
        'ticker': news_data['ticker'],
        'total_articles': news_data['total_articles'],
        'articles': []
    }
    
    for idx, article in enumerate(news_data['articles']):
        importance = importance_data['decisions'][idx]['importance']

        if importance and article['url']:
            article_text = scrape_yfinance_article(article['url'])
        else:
            article_text = ""

        merged_data['articles'].append({
            'title': article['title'],
            'summary': article['summary'],
            'provider': article['provider'],
            'editorsPick': article['editorsPick'],
            'importance': importance,
            'reason': importance_data['decisions'][idx]['reason'],
            'article_text': article_text,
        })
    
    return json.dumps(merged_data, indent=2)