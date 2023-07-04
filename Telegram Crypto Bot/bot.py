from telethon.sync import TelegramClient, events
from binance.helpers import round_step_size
from binance.client import Client

api_id = 19860939
channel_id = 1896179282
channel_name = "CryptoMasterBillboardx"
api_hash = 'b393ffdc9ab306b11c0ee1e21c942995'
api_key = 'AXfVzZojq6e4CHcGMefgX2VukvjMOx00EY9jNKzGPXWTaOWhK2WsVOn9OBXE4HAU'
api_secret = '6DZBbwuMobc53u4ljYdb5sepmmOpDtyFuigyIIuXJTkOmtxrlJLSNjraQ0k7x3pI'

# Create a new Telegram client object
client = TelegramClient("session_name", api_id, api_hash)


@client.on(events.NewMessage(chats=[channel_id]))
async def handle_new_message(event):
    # your code here
    # name of channel

    message = str(event.raw_text)
    try:
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

    except:
        pass


# Binance Bot:

def get_ip_address():
    import requests
    ip = requests.get('https://api.ipify.org').text
    print('My public IP address is: {}'.format(ip))
    return ip


get_ip_address()

# Connect to the Binance API
# binance_client = Client(api_key, api_secret)
# print("Binance Client Created")

# Start the client
client.start()
print("Client Created")

print(client.get_me())
# Run the client until interrupted by the user
# name of channel

client.run_until_disconnected()
