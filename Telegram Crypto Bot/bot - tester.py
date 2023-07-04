from binance.client import Client
from binance.helpers import round_step_size
# Connect to the Binance API
from binance.enums import *

channel_id = 1896179282
channel_name = "CryptoMasterBillboardx"
api_id = 19860939
api_hash = 'b393ffdc9ab306b11c0ee1e21c942995'
api_key = 'AXfVzZojq6e4CHcGMefgX2VukvjMOx00EY9jNKzGPXWTaOWhK2WsVOn9OBXE4HAU'
api_secret = '6DZBbwuMobc53u4ljYdb5sepmmOpDtyFuigyIIuXJTkOmtxrlJLSNjraQ0k7x3pI'
side, symbol, entry, stop_loss, profit_1, profit_2, profit_3, profit_4 = ['BUY', 'KLAYUSDT', '0.26450', '5-7%',
                                                                          '0.26979', '0.272435', '0.27508', '0.277725']

binance_client = Client(api_key, api_secret)
current_all_orders = binance_client.get_open_orders()
print(current_all_orders)

# current wallet balance from Binance
wallet_balance = binance_client.futures_account_balance()
print(wallet_balance)

x = binance_client.get_symbol_info(symbol)
y = binance_client.get_symbol_info('PERPUSDT')

current_price = binance_client.get_symbol_ticker(symbol=symbol)['price']
print(current_price)

print(x)
print(y)

quantity = 26

print(quantity)
print("Binance Client Created")

binance_client.futures_create_order(
    symbol=symbol,
    positionSide='LONG',
    type='TAKE_PROFIT_MARKET',
    timeInForce='GTE_GTC',
    quantity=quantity,
    stopPrice=stop_loss,

)

print("Stop Loss Order Placed")
quit()

# all orders are placed as market orders
orders = binance_client.futures_get_open_orders(symbol=symbol)
print(orders)
quit()
# take profit 1
binance_client.futures_create_order(
    symbol=symbol,
    side=side,
    type='TAKE_PROFIT_MARKET',
    quantity=quantity,
    stopPrice=profit_1,
    priceProtect=True,
    newOrderRespType='FULL'
)

# take profit 2
binance_client.futures_create_order(
    symbol=symbol,
    side=side,
    type='TAKE_PROFIT_MARKET',
    quantity=quantity,
    stopPrice=profit_2,
    priceProtect=True,
    newOrderRespType='FULL'
)

# take profit 3
binance_client.futures_create_order(
    symbol=symbol,
    side=side,
    type='TAKE_PROFIT_MARKET',
    quantity=quantity,
    stopPrice=profit_3,
    priceProtect=True,
    newOrderRespType='FULL'
)

# take profit 4
binance_client.futures_create_order(
    symbol=symbol,
    side=side,
    type='TAKE_PROFIT_MARKET',
    quantity=quantity,
    stopPrice=profit_4,
    priceProtect=True,
    newOrderRespType='FULL'
)
print("Order Placed")
