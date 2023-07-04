import math
import time

from binance.helpers import round_step_size
import binance
from binance.enums import *
from binance.client import Client

def get_ip_address():
    import requests
    ip = requests.get('https://api.ipify.org').text
    print('My public IP address is: {}'.format(ip))
    return ip

get_ip_address()
# Replace with your Binance API key and secret key
api_key = 'AXfVzZojq6e4CHcGMefgX2VukvjMOx00EY9jNKzGPXWTaOWhK2WsVOn9OBXE4HAU'
api_secret = '6DZBbwuMobc53u4ljYdb5sepmmOpDtyFuigyIIuXJTkOmtxrlJLSNjraQ0k7x3pI'
# api_key = 'f4sDDXwy30QmN3PZnG2mZXbFkwDHkShLe0HPF7laD3JX4tih8MyKxCap7ZDO6FF3'
# api_secret = 'd5yOIUycj88TysHwszIeBQ0QznanIDOmrMazRJ54qi0ZtiBHXLPsruAoeWxvjvQr'

# Connect to the Binance API
binance_client = Client(api_key, api_secret)

print("Client Created")

side, symbol, entry, stop_loss, profit_1, profit_2, profit_3, profit_4 = ['BUY', 'KLAYUSDT', '0.26450', '0.24768',
                                                                          '0.26979', '0.272435', '0.27508', '0.277725']



# Precision of the price
price_precision = binance_client.get_symbol_info(symbol)['filters'][0]['tickSize']
price_precision = len(price_precision) - 2
print("Price Precision: ", price_precision)


# place stop loss order
# Get the current market price
market_price = float(binance_client.futures_symbol_ticker(symbol=symbol)['price'])
print("Market Price: ", market_price)
# Set the stop price to be a certain percentage away from the market price
stop_price = round(market_price * 1.07, 4)  # 5% below the market price
print("Stop Price: ", stop_price)

# Place the stop loss order
quantity = 26.6
binance_client.futures_create_order(
    symbol=symbol,
    side=side,
    type='STOP_MARKET',
    quantity=quantity,
    stopPrice=stop_price,
)

print("Stop Loss Order Placed")
