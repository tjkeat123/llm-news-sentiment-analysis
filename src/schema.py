from pydantic import BaseModel, Field
from typing import List

class ArticleDecision(BaseModel):
    article_index: int = Field(description="The index of the news article in the array (0-based index)")
    importance: bool = Field(description="Whether the news article is important.")
    reason: str = Field(description="The reason why the news article is important or not.")

class NewsImportanceResponse(BaseModel):
    ticker: str = Field(description="The stock ticker symbol")
    decisions: List[ArticleDecision] = Field(description="List of decisions for each news article")

class NewsAnalysisScoreResponse(BaseModel):
    ticker: str = Field(description="The stock ticker symbol")
    score: int = Field(description="The bullish/bearish score between 0 and 100")
    sentiment: str = Field(description="The sentiment of the score 'Bullish' / 'Bearish' / 'Neutral'")
    confidence: str = Field(description="The confidence level of 'High' / 'Medium' / 'Low' on the score")
    reason: str = Field(description="The reason for the score")