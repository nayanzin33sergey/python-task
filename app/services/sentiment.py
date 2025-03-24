import httpx
from app.config import settings

class SentimentService:
    def __init__(self):
        self.datura_api_key = settings.DATURA_API_KEY
        self.chutes_api_key = settings.CHUTES_API_KEY

    async def get_tweets(self, netuid: int) -> list:
        """Get tweets about the subnet using Datura.ai"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.datura.ai/twitter/search",
                params={
                    "query": f"Bittensor netuid {netuid}",
                    "limit": 10
                },
                headers={"Authorization": f"Bearer {self.datura_api_key}"}
            )
            return response.json()["tweets"]

    async def analyze_sentiment(self, tweets: list) -> float:
        """Analyze tweet sentiment using Chutes.ai"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.chutes.ai/analyze",
                json={"texts": tweets},
                headers={"Authorization": f"Bearer {self.chutes_api_key}"}
            )
            scores = response.json()["sentiment_scores"]
            return sum(scores) / len(scores)  # Average sentiment 