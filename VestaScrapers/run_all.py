import os
import pywintypes
import requests


# find Scaper.py files in all folders of the current directory

# toast = ToastNotifier()
# toast.show_toast("Scrapers", "Running all scrapers", duration=30)


bot_token = '6166663681:AAF9vLxyN3CfA_Xb8Lomwuy3BD_MajoLF9w'
bot_chatID = '-1001885631289'


def telegram_bot_sendtext(bot_message):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


os.chdir(r"C:\Users\Administrator\PycharmProjects\Scrapers\Scrapers--Anshu-\PreStage")
scraper_files = []
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith("Scraper.py"):
            if "Whittle" in str(root):
                continue
            scraper_files.append(os.path.join(root, file))

# pip freeze > requirements.txt // pip install -r requirements.txt
# run all scraper files
# run all scraper files
for file in scraper_files:
    file_dir = os.path.dirname(file)
    print(file)
    
    os.chdir(file_dir)

    os.system("python Scraper.py")
    print(f"Ran {file}")
# run final_checks.py

# back to original directory
original_dir = r"C:\Users\Administrator\PycharmProjects\Scrapers\Scrapers--Anshu-\PreStage"
os.chdir(original_dir)
os.system("python final_checks.py")
print("Runned")