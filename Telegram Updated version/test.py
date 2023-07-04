import time

import binance
from binance.enums import *
from binance.client import Client

message = """
🔥 #FTM/USDT (Long📈, x20) 🔥

Entry - 0.456000
SL - 5-7%

Take-Profit:
🥇 0.46512 (40% of profit) 
🥈 0.46968 (60% of profit)
🥉 0.47424 (80% of profit)
🚀 0.4788 (100% of profit)
""".strip()


def calculate_stop_loss(entry_price_x, stop_loss_percent_x):
    stop_loss_amount_x = entry_price_x * stop_loss_percent_x
    stop_loss_price_x = entry_price_x - stop_loss_amount_x
    return stop_loss_price_x


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
        msg_part = msg_part.split('-')[0]
        # convert to percent
        msg_part = float(msg_part) / 100
        # calculate stop loss price
        msg_part = calculate_stop_loss(float(requirements[2]), msg_part)

        requirements.append(msg_part)

    if '% of profit' in i:
        msg_part = str(i.split(' ')[1].split(' ')[0]).strip()
        requirements.append(msg_part)

# ['BUY', 'ALPHAUSDT', '0.003856', '5-7%', '0.003933', '0.003972', '0.00401', '0.004049']
symbol, entry, sl, tp1, tp2, tp3, tp4 = requirements[1], requirements[2], requirements[3], requirements[4], \
requirements[5], requirements[6], requirements[7]
print(requirements)

# Replace with your Binance API key and secret key
api_key = 'AXfVzZojq6e4CHcGMefgX2VukvjMOx00EY9jNKzGPXWTaOWhK2WsVOn9OBXE4HAU'
api_secret = '6DZBbwuMobc53u4ljYdb5sepmmOpDtyFuigyIIuXJTkOmtxrlJLSNjraQ0k7x3pI'

# Connect to the Binance API
client = Client(api_key, api_secret)

# current orders on the account
orders = client.futures_get_open_orders()
print(orders)

print(len(orders))


# cancel all orders
for i in orders:
    client.futures_cancel_order(symbol=symbol, orderId=i['orderId'])
    print("Order " + str(i['orderId']) + " is cancelled")
    time.sleep(1)


quit()

def decide_quantity(coin_name, usd):
    # Get the current price and LOT_SIZE filter for the trading pair
    ticker = client.get_symbol_ticker(symbol=coin_name)
    info = client.get_symbol_info(symbol=coin_name)
    lot_size_filter = next(filter(lambda f: f['filterType'] == 'LOT_SIZE', info['filters']))


    # Calculate the maximum quantity based on available USDT
    current_price = float(ticker['price'])
    max_quantity = float(usd) / current_price

    # Round the quantity to the nearest valid lot size
    step_size = float(lot_size_filter['stepSize'])
    quantity = round(max_quantity / step_size) * step_size



    return quantity
# print(decide_quantity(symbol, 6))
# print("Quantity is calculated")
#
# current_price = float(client.get_symbol_ticker(symbol=symbol)['price'])
# print("Current price is " + str(current_price)  + " USDT")




# create order to buy


# Calculate the quantity of the trade
quantity = decide_quantity(symbol, 6)  # Replace 100 with the available USDT

# Place a market order for buying the symbol at the entry price
# order = client.futures_create_order(
#     symbol=symbol,
#     side=SIDE_BUY,
#     type=ORDER_TYPE_MARKET,
#     quantity=quantity
#
# )
# print("Order is placed")


# Place a stop loss order at the specified level
stop_loss = client.futures_create_order(
    symbol=symbol,
    side=SIDE_SELL,
    type ='STOP_MARKET',
    quantity=quantity,
    stopPrice=sl,
)



print("Stop loss order is placed")
# Place take profit limit orders at the specified levels
tp1_order = client.futures_create_order(
    symbol=symbol,
    side=SIDE_SELL,
    type=ORDER_TYPE_LIMIT,
    quantity=quantity,

)

print("Take profit 1 order is placed")