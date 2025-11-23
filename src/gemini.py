from google import genai
from google.genai import types
from dotenv import load_dotenv

import json
import os

from .schema import NewsImportanceResponse

# Load environment variables from .env file
load_dotenv()

class Gemini:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Get API key from environment variable
            api_key = os.getenv('GEMINI_API_KEY')
            if not api_key:
                raise ValueError(
                    "API key not found! Please create a .env file with:\n"
                    "GEMINI_API_KEY=your_api_key_here\n"
                    "Get your key from: https://aistudio.google.com/app/apikey"
                )
            cls._instance.client = genai.Client(api_key=api_key)
        return cls._instance

    def decide_news_importance(self, news_articles_json):
        """
        Decide if the news article is worth reading based on the title and summary.
        The importance is a boolean value.
        Check the schema for the response.
        """
        
        news_data = json.loads(news_articles_json)
        ticker = news_data.get('ticker', 'Unknown')
        total_articles = news_data.get('total_articles', 0)

        prompt = f"""Here are the titles and summaries of {total_articles} news articles for {ticker}.

        {news_articles_json}

        Please analyze EACH article and decide if it is worth reading based on the title and summary.
        For each article, provide:
        1. The article_index (0-based index matching the array position)
        2. A boolean indicating if it's important (True or False)
        3. A brief reason for your decision
        
        Decide based on the following criteria:
        - The relevance of the news article to the ticker
        - The credibility of the news article
        - The potential impact of the news article on the ticker
        - Is the news just some analyst's opinion or a fact?
        - Is the news an editor's pick?
        
        You must provide a decision for ALL {total_articles} articles.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a helpful research assistant that decides if a news article is worth reading based on the title and summary.",
                response_mime_type="application/json",
                response_schema=NewsImportanceResponse
            )
        )

        return response.text