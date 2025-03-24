from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from app.config import settings
import logging

logger = logging.getLogger(__name__)
api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    logger.info(f"Received token: {api_key_header}")
    logger.info(f"Expected token: Bearer {settings.API_TOKEN}")
    
    if not api_key_header or api_key_header != f"Bearer {settings.API_TOKEN}":
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API key"
        )
    return api_key_header 