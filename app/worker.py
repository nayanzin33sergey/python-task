from celery import Celery
from app.config import settings
from app.services.sentiment import SentimentService
from app.services.blockchain import BlockchainService

celery_app = Celery(
    "worker",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
)

@celery_app.task
async def analyze_and_stake(netuid: int, hotkey: str):
    """Background task to analyze sentiment and stake/unstake"""
    sentiment_service = SentimentService()
    blockchain_service = BlockchainService()

    # Get and analyze tweets
    tweets = await sentiment_service.get_tweets(netuid)
    sentiment_score = await sentiment_service.analyze_sentiment(tweets)

    # Calculate stake amount
    stake_amount = 0.01 * sentiment_score

    # Stake or unstake based on sentiment
    if stake_amount > 0:
        await blockchain_service.stake(stake_amount, netuid, hotkey)
    elif stake_amount < 0:
        await blockchain_service.unstake(abs(stake_amount), netuid, hotkey) 