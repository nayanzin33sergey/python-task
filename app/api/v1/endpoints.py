from fastapi import APIRouter, Depends, Query, HTTPException
from app.core.security import get_api_key
from app.services.blockchain import BlockchainService
from app.services.cache import CacheService
from app.services.database import Database
from app.worker import analyze_and_stake
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/tao_dividends")
async def get_tao_dividends(
    netuid: int = Query(default=18),
    hotkey: str = Query(default="5FFApaS75bv5pJHfAp2FVLBj9ZaXuFDjEypsaBNc1wCfe52v"),
    trade: bool = Query(default=False),
    api_key: str = Depends(get_api_key)
):
    """Get Tao dividends for a subnet and hotkey"""

    logger.info(f"Received request with netuid: {netuid}, hotkey: {hotkey}, trade: {trade}")
    
    # Check cache first
    cached_data = CacheService.get_from_cache(netuid, hotkey)
    if cached_data:
        return {**cached_data, "cached": True}
    
    logger.info("Cache miss, querying blockchain")

    # Query blockchain
    try:
        blockchain_service = BlockchainService()
        dividend = await blockchain_service.get_tao_dividends(netuid, hotkey)
    except Exception as e:
        logger.error(f"Error querying blockchain: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    # Store in cache and database
    data = {
        "netuid": netuid,
        "hotkey": hotkey,
        "dividend": dividend
    }
    CacheService.store_in_cache(netuid, hotkey, data)
    await Database.store_dividend_data(netuid, hotkey, dividend)

    # Trigger sentiment analysis and stake/unstake if requested
    if trade:
        # Add detailed logging for trade path
        logger.info(f"Trade requested with netuid={netuid}, hotkey={hotkey}")
        try:
            analyze_and_stake.delay(netuid, hotkey)
        except Exception as e:
            logger.error(f"Error during trade execution: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail=str(e))

    return {**data, "cached": False, "stake_tx_triggered": trade} 