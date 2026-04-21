from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from .logging_config import logger
import click

def place_order(client: Client, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
    """
    Places an order on the Binance Futures Testnet.
    """
    logger.info(f"Attempting to place order: symbol={symbol}, side={side}, type={order_type}, qty={quantity}, price={price}")
    
    try:
        kwargs = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }
        
        if order_type == 'LIMIT':
            if price is None:
                raise ValueError("Price must be specified for LIMIT orders.")
            kwargs['price'] = price
            kwargs['timeInForce'] = 'GTC'  # Good Till Cancelled is required for limit orders
        
        # Place the order using futures_create_order
        response = client.futures_create_order(**kwargs)
        
        logger.info(f"Order successful: {response}")
        return response

    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: {e.status_code} - {e.message}")
        raise e
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception: {e}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error placing order: {e}")
        raise e
