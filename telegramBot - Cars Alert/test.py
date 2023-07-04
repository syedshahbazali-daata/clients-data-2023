import concurrent.futures
import requests


bot_token = '5792992329:AAGGGWh_qA5G0V3cfva3GfjuU7KKERpdVlI'
bot_chatID = '-1001988258620'
def telegram_bot_sendtext_x(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage'
    params = {
        'chat_id': bot_chatID,
        'parse_mode': 'HTML',
        'text': bot_message
    }
    response = requests.post(send_text, data=params)
    return response.json()



def send_message(messages):
    # Create a thread pool executor with maximum concurrency of 5
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit the tasks
        futures = [executor.submit(telegram_bot_sendtext_x, message) for message in messages]

        # Wait for all tasks to complete
        concurrent.futures.wait(futures)

        # Get the results
        results = [future.result() for future in futures]

        # Process the results if needed
        for result in results:
            print(result)
