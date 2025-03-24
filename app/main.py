from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.services.cache import redis_client
from app.services.database import client

from app.api.v1 import endpoints
from app.core.logging import setup_logging

# Setup logging
logger = setup_logging()

app = FastAPI(
    title="Tao Dividends API",
    description="API for querying Tao dividends and managing stake operations",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(endpoints.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Test Redis connection
    try:
        redis_client.ping()
        print("Successfully connected to Redis")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")

    # Test MongoDB connection
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 