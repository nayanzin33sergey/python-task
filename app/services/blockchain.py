from bittensor import AsyncSubtensor
from app.config import settings
from app.core.logging import setup_logging
from bittensor_wallet import Wallet
from bittensor.utils.balance import Balance
from bittensor_wallet.keypair import Keypair

# Initialize logger
logger = setup_logging()

class BlockchainService:
    def __init__(self):
        self.subtensor = AsyncSubtensor()
        # Create wallet with keypair from seed
        self.wallet = Wallet()
        # First regenerate the hotkey
        self.wallet.regenerate_hotkey(
            mnemonic="diamond like interest affair safe clarify lawsuit innocent beef van grief color",
            use_password=False,
            overwrite=True
        )
        # Then regenerate coldkey with same mnemonic
        self.wallet.regenerate_coldkey(
            mnemonic="diamond like interest affair safe clarify lawsuit innocent beef van grief color",
            use_password=False,
            overwrite=True
        )

    async def get_tao_dividends(self, netuid: int, hotkey: str) -> float:
        """Query Tao dividends from the blockchain"""
        try:
            logger.info(f"Querying TaoDividendsPerSubnet for netuid: {netuid} and hotkey: {hotkey}")
            dividend = await self.subtensor.query_subtensor(
                name="TaoDividendsPerSubnet",
                params=[netuid, hotkey]
            )
            return float(dividend.value) if dividend else 0.0
        except Exception as e:
            logger.error(f"Error querying blockchain: {e}")
            raise

    async def stake(self, amount: float, netuid: int = 18, hotkey: str = settings.DEFAULT_HOTKEY):
        """Submit stake extrinsic"""
        try:
            logger.info(f"Staking {amount} TAO to hotkey {hotkey} on subnet {netuid}")
            await self.subtensor.add_stake(
                wallet=self.wallet,
                amount=Balance.from_tao(amount),
                netuid=netuid,
                hotkey_ss58=hotkey,
                wait_for_inclusion=True,
                wait_for_finalization=False
            )
        except Exception as e:
            logger.error(f"Error staking: {e}")
            raise

    async def unstake(self, amount: float, netuid: int = 18, hotkey: str = settings.DEFAULT_HOTKEY):
        """Submit unstake extrinsic"""
        try:
            logger.info(f"Unstaking {amount} TAO from hotkey {hotkey} on subnet {netuid}")
            await self.subtensor.unstake(
                wallet=self.wallet,
                amount=Balance.from_tao(amount),
                netuid=netuid,
                hotkey_ss58=hotkey,
                wait_for_inclusion=True,
                wait_for_finalization=False
            )
        except Exception as e:
            logger.error(f"Error unstaking: {e}")
            raise 