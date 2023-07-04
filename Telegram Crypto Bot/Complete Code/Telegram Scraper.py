from telethon.sync import TelegramClient, events

api_id = 17213627  # Replace with your telegraph API ID
api_hash = '508872114878f0203f45231d2d4e68e9'  # Replace with your telegraph API Hash

channel_name = "CryptoMasterBillboardx"

# Create a new Telegram client object
client = TelegramClient("session_name", api_id, api_hash)

# Use the `events.NewMessage` event to capture new messages in the channel

# channel is private but I'm member of it
from telethon import types

# Replace 'channel_id' with the ID of the channel you want to scrape messages from
channel_id = -1001717037581


@client.on(events.NewMessage(chats=[channel_id]))
async def handle_new_message(event):
    # your code here

    message = str(event.raw_text)
    try:
        message = message.split('\n')
        if len(message) > 3:
            return
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


# scrape all messages from channel


# Start the client
client.start()
print("Client Created")

# print account number
print(client.get_me())
# Run the client until interrupted by the user
client.run_until_disconnected()
