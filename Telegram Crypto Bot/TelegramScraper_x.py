from telethon.sync import TelegramClient, events

telegram_api_id = 19860939
telegram_channel_id = 1896179282

telegram_api_hash = 'b393ffdc9ab306b11c0ee1e21c942995'
telegram_api_key = 'AXfVzZojq6e4CHcGMefgX2VukvjMOx00EY9jNKzGPXWTaOWhK2WsVOn9OBXE4HAU'
telegram_api_secret = '6DZBbwuMobc53u4ljYdb5sepmmOpDtyFuigyIIuXJTkOmtxrlJLSNjraQ0k7x3pI'

# Create a new Telegram client object
telegram_client = TelegramClient("session_name", telegram_api_id, telegram_api_hash)


def message_config(text):
    try:
        message = text.split('\n')
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

        return requirements

    except:
        return None


@telegram_client.on(events.NewMessage(chats=[telegram_channel_id]))
async def handle_new_message(event):
    message = str(event.raw_text)
    telegram_trade_message = message_config(message)
    if telegram_trade_message is not None:
        print(telegram_trade_message)





telegram_client.start()
print('Telegram client started')

telegram_client.run_until_disconnected()
