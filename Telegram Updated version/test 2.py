import os
from math import floor, log10

from binance.client import Client


def round_price(price, tick_size):
    return round(price // tick_size * tick_size, -int(floor(log10(tick_size))))


api_key = 'AXfVzZojq6e4CHcGMefgX2VukvjMOx00EY9jNKzGPXWTaOWhK2WsVOn9OBXE4HAU'
api_secret = '6DZBbwuMobc53u4ljYdb5sepmmOpDtyFuigyIIuXJTkOmtxrlJLSNjraQ0k7x3pI'

client = Client(api_key, api_secret)

symbol = "FTMUSDT"
leverage = 20
entry = 0.456000
stop_loss = 0.456000 * (1 - 0.07)
take_profit = [(0.46512, 0.4), (0.46968, 0.6), (0.47424, 0.8), (0.4788, 1.0)]
min_notional = 6.0
min_quantity = 14
print(min_quantity)
# Get symbol information
symbol_info = client.get_symbol_info(symbol)
tick_size = float(next(filter(lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']))['tickSize'])
quantity_precision = int(
    next(filter(lambda f: f['filterType'] == 'LOT_SIZE', symbol_info['filters']))['stepSize'].find('.') + 1)
price_precision = int(
    next(filter(lambda f: f['filterType'] == 'PRICE_FILTER', symbol_info['filters']))['tickSize'].find('.') + 1)

print(client.get_symbol_info(symbol))


def round_to_precision(value, precision):
    print(precision)
    result = round(value, precision)
    print(result)
    return result


# Round prices according to tick size
entry = round_price(entry, tick_size)
stop_loss = round_price(stop_loss, tick_size)
take_profit = [(round_price(tp, tick_size), profit_ratio) for tp, profit_ratio in take_profit]

# Set leverage
client.futures_change_leverage(symbol=symbol, leverage=leverage)

# Place a long order
order = client.futures_create_order(
    symbol=symbol,
    side=Client.SIDE_BUY,
    type=Client.ORDER_TYPE_LIMIT,
    timeInForce=Client.TIME_IN_FORCE_GTC,
    quantity=round_to_precision(min_quantity, quantity_precision),
    price=entry,
)

order_id = order['orderId']
print(f"Order placed successfully. Order ID: {order_id}")

# Set stop loss
client.futures_create_order(
    symbol=symbol,
    side=Client.SIDE_SELL,
    type=Client.FUTURE_ORDER_TYPE_STOP_MARKET,
    stopPrice=stop_loss,
    quantity=round_to_precision(min_quantity, quantity_precision),  # Round the quantity to the allowed precision
    customClientOrderId=f"stop_loss_{order_id}",
)

print("Stop loss order placed successfully.")
# Set take profit orders
for tp, profit_ratio in take_profit:
    quantity_z = round_to_precision(min_quantity * profit_ratio, quantity_precision)
    notional = tp * quantity_z
    print(f"Quantity: {quantity_z}")
    print(f"Notional: {notional}")
    if notional >= min_notional:
        client.futures_create_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_LIMIT,
            timeInForce=Client.TIME_IN_FORCE_GTC,
            quantity=quantity_z,
            price=tp,
            customClientOrderId=f"take_profit_{tp}_{order_id}",
        )
    else:
        print(f"Notional value for take-profit order at {tp} is below the minimum allowed: {notional}")

print("Orders placed successfully.")
