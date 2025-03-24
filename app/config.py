from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class Settings(BaseModel):
    # API Settings
    API_TOKEN: str = os.getenv("API_TOKEN", "test123")
    PORT: int = int(os.getenv("PORT", "8000"))

    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # Database Settings
    DATABASE_URL: str = "mongodb://localhost:27017/tao_dividends"

    # External API Settings
    DATURA_API_KEY: Optional[str] = None
    CHUTES_API_KEY: Optional[str] = None

    # Bittensor Settings
    DEFAULT_HOTKEY: Optional[str] = None
    DEFAULT_NETUID: int = 18
    WALLET_SEED: Optional[str] = None
    WALLET_NAME: Optional[str] = None

    class Config:
        env_file = ".env"

# Create settings instance
settings = Settings() 