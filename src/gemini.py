from google import genai
from google.genai import types
from dotenv import load_dotenv

import json
import os

from .schema import NewsImportanceResponse, NewsAnalysisScoreResponse

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

    def get_analysis_score(self, news_articles_json):
        """
        Get the analysis of the news articles.
        The analysis is a string of the analysis of the news articles.
        """
        news_data = json.loads(news_articles_json)
        ticker = news_data.get('ticker', 'Unknown')
        total_articles = news_data.get('total_articles', 0)

        prompt = f"""You will be given:
        - A stock ticker: {ticker}
        - A list of {total_articles} news articles or summaries in JSON format: {news_articles_json}

        TASK:
        Analyze EACH article individually and assign a bullish/bearish impact score from 0 to 100 for the given ticker.

        SCORING GUIDELINES:
        - 0-20   = Very Bearish (major negative impact, confirmed bad news)
        - 21-40  = Bearish (moderate negative impact)
        - 41-59  = Neutral / No clear market impact
        - 60-79  = Bullish (moderate positive impact)
        - 80-100 = Very Bullish (strong positive impact, major catalyst)

        EVALUATION CRITERIA (must be explicitly considered):
        1. Relevance: How directly the article affects the ticker
        2. Credibility of the source (official filings, major news > blogs > social media)
        3. Factual vs Opinion-based (facts weighted more than analyst opinions)
        4. Expected vs Surprise (unexpected news has higher impact)
        5. Magnitude of financial or operational impact
        6. Time sensitivity (recent news > old news)

        SPECIAL RULES:
        - If the article is not materially relevant to the ticker, assign a score between 45-55.
        - If the article is purely speculative or opinion-based, explain that clearly in the reason.
        - Do NOT invent financial data.
        - Base your reasoning strictly on the provided article text.
        """

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction="You are a financial news sentiment analyst.",
                response_mime_type="application/json",
                response_schema=NewsAnalysisScoreResponse
            )
        )

        return response.text