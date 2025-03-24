from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from datetime import datetime

# Create MongoDB client
client = AsyncIOMotorClient(settings.DATABASE_URL)
db = client.tao_dividends

class Database:
    @staticmethod
    async def store_dividend_data(netuid: int, hotkey: str, dividend: float):
        """Store dividend data in MongoDB"""
        await db.dividends.update_one(
            {"netuid": netuid, "hotkey": hotkey},
            {
                "$set": {
                    "dividend": dividend,
                    "updated_at": datetime.utcnow()
                }
            },
            upsert=True
        )

    @staticmethod
    async def get_dividend_data(netuid: int = None, hotkey: str = None):
        """Retrieve dividend data from MongoDB"""
        query = {}
        if netuid is not None:
            query["netuid"] = netuid
        if hotkey is not None:
            query["hotkey"] = hotkey
            
        cursor = db.dividends.find(query)
        return await cursor.to_list(length=None) 