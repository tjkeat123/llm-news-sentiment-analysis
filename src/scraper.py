import requests
from bs4 import BeautifulSoup

def scrape_yfinance_article(url: str) -> str:
    """Scrape the given Yahoo Finance URL and return the article text."""
    
    article = ""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()  # Ensure we notice bad responses

        soup = BeautifulSoup(response.text, 'html.parser')
        article_body = soup.find('div', {'data-testid': 'article-body'})
        all_paragraphs = article_body.find_all('p')
        for p in all_paragraphs:
            article += p.get_text() + '\n'
    except requests.RequestException as e:
        article = f'Error fetching the URL: {e}'
    return article