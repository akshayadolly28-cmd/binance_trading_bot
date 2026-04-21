import click
import os
from dotenv import load_dotenv
from bot.client import BinanceTestnetClient
from bot.orders import place_order
from bot.validators import validate_symbol, validate_price_if_limit
from bot.logging_config import logger
from binance.exceptions import BinanceAPIException, BinanceRequestException
import colorama

# Initialize colorama for colored terminal output
colorama.init(autoreset=True)

@click.command()
@click.option('--symbol', required=True, callback=validate_symbol, help='Trading pair symbol, e.g., BTCUSDT')
@click.option('--side', required=True, type=click.Choice(['BUY', 'SELL'], case_sensitive=False), help='Order side: BUY or SELL')
@click.option('--type', 'order_type', required=True, type=click.Choice(['MARKET', 'LIMIT'], case_sensitive=False), help='Order type: MARKET or LIMIT')
@click.option('--quantity', required=True, type=float, help='Order quantity')
@click.option('--price', type=float, help='Order price (required for LIMIT orders)')
def main(symbol, side, order_type, quantity, price):
    """
    Binance Futures Testnet Trading Bot CLI.
    
    Places MARKET or LIMIT orders. Ensure you have BINANCE_TESTNET_API_KEY 
    and BINANCE_TESTNET_API_SECRET set in your .env file.
    """
    side = side.upper()
    order_type = order_type.upper()
    
    validate_price_if_limit(order_type, price)

    click.echo(colorama.Fore.CYAN + "--- Order Request Summary ---")
    click.echo(f"Symbol:   {symbol}")
    click.echo(f"Side:     {side}")
    click.echo(f"Type:     {order_type}")
    click.echo(f"Quantity: {quantity}")
    if order_type == 'LIMIT':
        click.echo(f"Price:    {price}")
    click.echo(colorama.Fore.CYAN + "-----------------------------")

    load_dotenv()
    api_key = os.getenv('BINANCE_TESTNET_API_KEY')
    api_secret = os.getenv('BINANCE_TESTNET_API_SECRET')

    if not api_key or not api_secret:
        click.echo(colorama.Fore.RED + "Error: API credentials not found. Please set BINANCE_TESTNET_API_KEY and BINANCE_TESTNET_API_SECRET in a .env file.")
        logger.error("API credentials missing.")
        return

    try:
        binance_client = BinanceTestnetClient(api_key, api_secret)
        client = binance_client.get_client()
        
        click.echo(colorama.Fore.YELLOW + "Placing order on Binance Futures Testnet...")
        
        response = place_order(
            client=client,
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        click.echo(colorama.Fore.GREEN + "\nSUCCESS: Order placed successfully!")
        click.echo(colorama.Fore.CYAN + "--- Order Response Details ---")
        click.echo(f"Order ID:     {response.get('orderId')}")
        click.echo(f"Status:       {response.get('status')}")
        click.echo(f"Executed Qty: {response.get('executedQty')}")
        avg_price = response.get('avgPrice')
        if avg_price:
             click.echo(f"Avg Price:    {avg_price}")
        
    except BinanceAPIException as e:
        click.echo(colorama.Fore.RED + f"\nFAILED: Binance API Error: {e.message} (Code: {e.status_code})")
    except BinanceRequestException as e:
        click.echo(colorama.Fore.RED + f"\nFAILED: Network error: {e}")
    except Exception as e:
        click.echo(colorama.Fore.RED + f"\nFAILED: An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()
