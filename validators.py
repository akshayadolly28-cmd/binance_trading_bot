import click

def validate_symbol(ctx, param, value):
    if not value or len(value) < 4:
        raise click.BadParameter("Symbol must be at least 4 characters long (e.g., BTCUSDT).")
    return value.upper()

def validate_price_if_limit(order_type, price):
    if order_type == 'LIMIT' and price is None:
        raise click.UsageError("--price is required when order-type is LIMIT.")
    if order_type in ['MARKET'] and price is not None:
        click.echo(click.style("Warning: Price is ignored for MARKET orders.", fg="yellow"))
