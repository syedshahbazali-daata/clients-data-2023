import time

import binance
from binance.enums import *
from binance.client import Client

# Replace with your Binance API key and secret key
api_key = 'AXfVzZojq6e4CHcGMefgX2VukvjMOx00EY9jNKzGPXWTaOWhK2WsVOn9OBXE4HAU'
api_secret = '6DZBbwuMobc53u4ljYdb5sepmmOpDtyFuigyIIuXJTkOmtxrlJLSNjraQ0k7x3pI'

# Connect to the Binance API
client = Client(api_key, api_secret)

# Get the server time and calculate the time difference
server_time = client.get_server_time()
time_diff = server_time['serverTime'] - int(time.time() * 1000)

print("Client Created")

# current price of STORJ
price_Z = client.get_symbol_ticker(symbol='STORJUSDT')
print(float(price_Z['price']))

print("API Connected")

def buy_order(symbol, quantity, stop_loss, take_profit):
    try:
        # Use the synchronized timestamp
        timestamp = int(time.time() * 1000 + time_diff)
        order = client.create_order(
            symbol=symbol,
            side=SIDE_BUY,
            type=ORDER_TYPE_STOP_LOSS_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=take_profit,
            stopPrice=stop_loss,
            timestamp=timestamp)
        print(order)
    except Exception as e:
        print(e)


def sell_order(symbol, quantity, stop_loss, take_profit):
    try:
        order = client.create_order(
            symbol=symbol,
            side=SIDE_SELL,
            type=ORDER_TYPE_STOP_LOSS_LIMIT,
            timeInForce=TIME_IN_FORCE_GTC,
            quantity=quantity,
            price=take_profit,
            stopPrice=stop_loss)
        print(order)
    except Exception as e:
        print(e)


buy_order('STORJUSDT', 100, 0.1, 0.2)

