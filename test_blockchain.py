import asyncio
from app.services.blockchain import BlockchainService
from app.config import settings

async def test_blockchain_service():
    service = BlockchainService()
    
    # Test 1: Query dividends
    try:
        print("\nTesting get_tao_dividends...")
        dividends = await service.get_tao_dividends(
            netuid=18, 
            hotkey=settings.DEFAULT_HOTKEY
        )
        print(f"Dividends: {dividends}")
    except Exception as e:
        print(f"Error querying dividends: {e}")

    # Test 2: Stake a small amount
    try:
        print("\nTesting stake...")
        amount = 0.1  # Stake 0.1 TAO
        await service.stake(
            amount=amount,
            netuid=18,
            hotkey=settings.DEFAULT_HOTKEY
        )
        print(f"Successfully staked {amount} TAO")
    except Exception as e:
        print(f"Error staking: {e}")

    # Test 3: Unstake the amount
    try:
        print("\nTesting unstake...")
        amount = 0.1  # Unstake 0.1 TAO
        await service.unstake(
            amount=amount,
            netuid=18,
            hotkey=settings.DEFAULT_HOTKEY
        )
        print(f"Successfully unstaked {amount} TAO")
    except Exception as e:
        print(f"Error unstaking: {e}")

if __name__ == "__main__":
    asyncio.run(test_blockchain_service()) 