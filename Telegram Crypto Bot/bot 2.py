import binance
from binance.enums import *

# Replace with your Binance API key and secret key
api_key = 'OzJT14tGN8H2mmmopgc2nmlQMF54Y7x2E6q3hqgjnYcVSE2ojI7BVIzXW27On9OH'
api_secret = 'p0O5r6tXqEnxtb110fHGrNN1lomouQun3QQWCh8a4agP4AYEKLy2ZtKJdnyMl98R'
# api_key = 'W0zljtumiPQ96dyDMhuZnsfaxaYN6XhYDeWOdEFOk1wkYhEuWE1AeohNrE3vxSWY'
# api_secret = 'V250QFGUlwsc8E2VZkxNBZk79I55UcCjtjgp73EabWsfv2jLp48ivoxieORDs3KR'

# Connect to the Binance API
client = binance.Client(api_key, api_secret)

print("Client Created")

# current price of STORJ
price = client.get_symbol_ticker(symbol='STORJUSDT')
print(price)


# current orders in the market

# Replace with the signal details
symbol = 'STORJUSDT'
side = 'BUY'
quantity = 1  # Replace with the amount of STORJ you want to buy
entry_price = 0.3754
stop_loss = 0.35  # 5-7% below the entry price
tp1_price = 0.382908
tp2_price = 0.386662
tp3_price = 0.390416
tp4_price = 0.39417

# Place the order
order = client.futures_create_order(
    symbol=symbol,
    side=side,
    type=ORDER_TYPE_MARKET,
    quantity=quantity,
)


print('Order placed successfully!')
orders = client.get_open_orders()
print(orders)


