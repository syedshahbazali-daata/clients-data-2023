import time

import binance
from binance.enums import *
from binance.client import Client

message = """
🔥 #RSR/USDT (Long📈, x20) 🔥

Entry - 0.003856
SL - 5-7%

Take-Profit:
🥇 0.003933 (40% of profit) 
🥈 0.003972 (60% of profit)
🥉 0.00401 (80% of profit)
🚀 0.004049 (100% of profit)
""".strip()

print(message.split('\n'))
message = message.split('\n')

requirements = []
for i in message:
    i = i.strip()


    if '#' in i:
        if 'long' in i.strip().lower():
            requirements.append('BUY')
        if 'short' in i.strip().lower():
            requirements.append('SELL')

        msg_part = i.split('#')[1].split(' ')[0].replace('/', '')
        requirements.append(msg_part)

    if 'Entry' in i:
        msg_part = i.split('Entry - ')[1]
        requirements.append(msg_part)

    if 'SL' in i:
        msg_part = i.split('SL - ')[1]
        requirements.append(msg_part)

    if '% of profit' in i:
        msg_part = str(i.split(' ')[1].split(' ')[0]).strip()
        requirements.append(msg_part)


print(requirements)


# Replace with your Binance API key and secret key
api_key = 'AXfVzZojq6e4CHcGMefgX2VukvjMOx00EY9jNKzGPXWTaOWhK2WsVOn9OBXE4HAU'
api_secret = '6DZBbwuMobc53u4ljYdb5sepmmOpDtyFuigyIIuXJTkOmtxrlJLSNjraQ0k7x3pI'

# Connect to the Binance API
client = Client(api_key, api_secret)


# ['BUY', 'RSRUSDT', '0.003856', '5-7%', '0.003933', '0.003972', '0.00401', '0.004049']: use this info to place order

# I want to buy the quantity only for 5 usd

def quantity_buy(coin_name, usd):
    current_price = client.get_symbol_ticker(symbol=coin_name)['price']
    min_quantity = client.get_symbol_info(coin_name)['filters'][2]['minQty']
    print(min_quantity)
    print(current_price)
    quantity = float(usd) / float(current_price)
    return quantity


# Place a test market buy order, to place an actual order use the create_order function with stop loss of 7%
order = client.create_test_order(
    symbol='RSRUSDT',
    side=SIDE_BUY,
    type=ORDER_TYPE_MARKET,
    quantity=quantity_buy('RSRUSDT', 5))







print("test order placed")




