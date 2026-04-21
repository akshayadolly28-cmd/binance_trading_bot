import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .logging_config import logger

class BinanceTestnetClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        # Initialize client with testnet=True
        try:
            self.client = Client(api_key, api_secret, testnet=True)
            logger.info("Binance Client initialized for Testnet.")
        except Exception as e:
            logger.error(f"Failed to initialize Binance Client: {e}")
            raise

    def get_client(self) -> Client:
        return self.client
