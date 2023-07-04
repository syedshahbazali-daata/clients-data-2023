import time
from binance.client import Client

# Replace with your Binance API key and secret key
api_key = 'AXfVzZojq6e4CHcGMefgX2VukvjMOx00EY9jNKzGPXWTaOWhK2WsVOn9OBXE4HAU'
api_secret = '6DZBbwuMobc53u4ljYdb5sepmmOpDtyFuigyIIuXJTkOmtxrlJLSNjraQ0k7x3pI'


client = Client(api_key, api_secret)

server_time = client.get_server_time()
time_diff = server_time['serverTime'] - int(time.time() * 1000)

timestamp = int(time.time() * 1000 + time_diff)

# Add a delay before making the API request
time.sleep(5)

try:
    client.create_order(
        symbol='BTCUSDT',
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_LIMIT,
        timeInForce=Client.TIME_IN_FORCE_GTC,
        quantity=1,
        price='50000',
        timestamp=timestamp
    )
except Exception as e:
    print(e)

print("Current Price of STORJ: ", client.get_symbol_ticker(symbol='STORJUSDT'))