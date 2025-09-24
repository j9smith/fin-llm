import os
from typing import List, Dict, Optional
import requests
import openai
import asyncio
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

class NewsService:
    def __init__(self):
        self.alpha_vantage_key = None
        self.base_url = "https://www.alphavantage.co/query"
        self.client = openai.AsyncOpenAI()

    async def summarize_article(self, article: Dict, user_message: str) -> Dict:
        """Summarize a single article asynchronously, including the article link if available."""
        print(f"Starting to summarize article: {article['title']}")
        # Check if the URL is available in the article data
        article_url = article.get("url", "URL not provided")
        
        try:
            prompt = f"""
            Given the context of this chat message: "{user_message}"
            Provide a concise 2-3 sentence summary of this financial news article:
            Title: {article['title']}
            Content: {article['summary']}
            """
            
            summary = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            print(f"Finished summarizing article: {article['title']}")
            return {
                "title": article["title"],
                "summary": summary.choices[0].message.content.strip(),
                "timestamp": article["time_published"],
                "source": article["source"],
                "url": article_url,  # Include the article link in the response
                "relevance": {
                    "topics": [],
                    "tickers": []
                }
            }
        except Exception as e:
            print(f"Error summarizing article: {e}")
            return {
                "title": article.get("title", "Unknown Title"),
                "summary": "Error generating summary.",
                "timestamp": article.get("time_published", "Unknown Timestamp"),
                "source": article.get("source", "Unknown Source"),
                "url": article_url,  # Include the article link even in case of errors
                "relevance": {
                    "topics": [],
                    "tickers": []
                }
            }

    async def get_news_summaries(self, chat_context: Dict) -> List[Dict]:
        print("Starting news retrieval")
        topics = chat_context.get('topics', [])
        tickers = chat_context.get('extracted_tickers', [])
        user_message = chat_context.get('message', '')

        # might want to add some parameter here to refine when the news is extracted (i.e. within last day, week, etc.)
        # additionally lots of parameters are available which we can choose to pass into the api call
        params = {
            "function": "NEWS_SENTIMENT",
            "apikey": self.alpha_vantage_key,
            "limit": 5,
            "sort": "RELEVANCE"
        }
        if tickers:
            params["tickers"] = ",".join(tickers)
        if topics:
            params["topics"] = ",".join(topics)

        try:
            print("Fetching news from Alpha Vantage")
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            news_data = response.json()

            if "feed" not in news_data:
                print("No news feed found in response")
                return []

            articles = news_data["feed"][:5]
            print(f"Processing {len(articles)} articles")

            summaries = []
            for article in articles:
                summary = await self.summarize_article(article, user_message)
                if summary:
                    summaries.append(summary)
                if len(summaries) >= 3:  # Limit to 3 articles for faster response
                    break

            print(f"Successfully processed {len(summaries)} summaries")
            return summaries

        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return []

# Initialize service
news_service = NewsService()