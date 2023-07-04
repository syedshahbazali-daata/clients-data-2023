from telethon.sync import TelegramClient, events

api_id = 17213627  # Replace with your telegraph API ID
api_hash = '508872114878f0203f45231d2d4e68e9'  # Replace with your telegraph API Hash
#
# api_id = 19860939
# api_hash = 'b393ffdc9ab306b11c0ee1e21c942995'

channel_name = "CryptoMasterBillboardx"

# Create a new Telegram client object
client = TelegramClient("client_session", api_id, api_hash)

# print all channels name and id
# +16049707232

#
client.start()
print("Client Created")
for dialog in client.iter_dialogs():
    print(dialog.name, 'has ID', dialog.id)

# Use the `events.NewMessage` event to capture new messages in the channel
