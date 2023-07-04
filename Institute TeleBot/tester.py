from datetime import datetime
import csv
import telebot
from telebot import types
import pandas as pd

# from keepAlive import *
# keep_alive()

api_key = "6151156163:AAGHaWCO0tCymZyJS-H3cN8DKOTFixLxRfA"

bot = telebot.TeleBot(api_key)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    lang_btn_ar = types.InlineKeyboardButton('Arabic', callback_data='lang_ar')
    lang_btn_en = types.InlineKeyboardButton('English', callback_data='lang_en')
    markup.add(lang_btn_ar, lang_btn_en)

    bot.reply_to(message, "Please select your preferred language:", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Arabic', 'English'])
def ask_menu(message, lang):
    if lang == 'ar':
        text_data = ['من نحن', 'زيارة الموقع', 'معلومات الاتصال', 'ماذا نقدم؟', 'العنوان', 'سجل الآن',
                     'كيف يمكنني مساعدتك اليوم؟']
    else:
        text_data = ['About Us', 'Visit Website', 'Contact Info', 'What We Offer?', 'Address', 'Register Now',
                     'How can I help you today?']

    markup = types.InlineKeyboardMarkup()

    option1 = types.InlineKeyboardButton(text_data[0], callback_data='option1')
    option2 = types.InlineKeyboardButton(text_data[1], url='http://qudrat.edu.sa/home')
    option3 = types.InlineKeyboardButton(text_data[2], callback_data='option3')
    option4 = types.InlineKeyboardButton(text_data[3], callback_data='option4')

    option5 = types.InlineKeyboardButton(text_data[4], url='https://goo.gl/maps/yFk7Y2FrXjcirMa8A?coh=178571&entry=tt')

    option6 = types.InlineKeyboardButton(text_data[5], callback_data='option6')

    markup.row(option1, option2)
    markup.row(option3, option4)
    markup.row(option5)
    markup.row(option6)

    bot.reply_to(message, text_data[6], reply_markup=markup)


lang = []


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    print(lang)

    if call.data == 'option1':
        if lang[0] == 'ar':
            text_data = [
                'معهد القدرات الإدارية يعزز تقديم التعليم والتعلم في مجال الإدارة والقيادة والتكنولجيا الحديثة.']
        else:
            text_data = [
                "The High Managerial Aptitude Institue for training Promotes the delivery of teaching and learning in management, leadership and modern technology."]
        # bot.answer_callback_query(call.id, 'You selected Option 1')
        message_about_us = text_data[0]
        bot.send_message(call.message.chat.id, message_about_us)

    elif call.data == 'option2':
        # bot.answer_callback_query(call.id, 'You selected Option 2')
        website_link = "http://qudrat.edu.sa/home"
        bot.send_message(call.message.chat.id, website_link)

    elif call.data == 'option3':
        # bot.answer_callback_query(call.id, 'You selected Option 3')
        contact_info = """Contact info :\nLadies branch : 0138312121\nMales branch : 0596828503\n\nEmail: Info@qudrat.edu.sa"""
        bot.send_message(call.message.chat.id, contact_info)

    elif call.data == 'option4':
        # bot.answer_callback_query(call.id, 'You selected Option 4')
        if lang[0] == 'ar':
            what_we_offer = """الدبلومات التي يقدمها المعهد:
- التكنولوجيا والذكاء الاصطناعي
- دبلوم العلوم الإدارية
- دبلوم الأمن السيبراني
- دبلوم تطبيقات الموبايل / الويب
- دبلوم الموارد البشرية
- دبلوم تقنية المعلومات"""
        else:

            what_we_offer = """Diplomas that institute offer : 
- Technology and Artificial Intelligence
- the administrative science diploma 
- Cyber Security Diploma 
- The Mobile/web Applications Diploma 
- Human resources Diploma 
- Diploma of Information Technology"""
        bot.send_message(call.message.chat.id, what_we_offer)

    elif call.data == 'option5':
        # bot.answer_callback_query(call.id, 'You selected Option 5')
        # open google maps
        bot.send_message(call.message.chat.id, "https://goo.gl/maps/yFk7Y2FrXjcirMa8A?coh=178571&entry=tt")

    elif call.data == 'option6':
        if lang[0] == 'ar':
            text_data = ['يرجى تقديم التفاصيل التالية:', 'الاسم']
        else:
            text_data = ['Please provide the following details:', 'Name']
        # bot.answer_callback_query(call.id, 'You selected Option 6')
        bot.send_message(call.message.chat.id, f"{text_data[0]}\n\n{text_data[1]}:")

        bot.register_next_step_handler(call.message, ask_major)

    elif call.data == 'lang_ar':
        lang.clear()
        ask_menu(call.message, 'ar')
        lang.append('ar')
        print(lang)
    elif call.data == 'lang_en':
        lang.clear()

        ask_menu(call.message, 'en')
        lang.append('en')
        print(lang)


def ask_major(message):
    if lang[0] == 'ar':
        text_data = ['التخصص']
    else:
        text_data = ['Major']
    name = message.text
    bot.send_message(message.chat.id, f"{text_data[0]}:")
    bot.register_next_step_handler(message, ask_phone_number, name)


def ask_phone_number(message, name):
    if lang[0] == 'ar':
        text_data = ['رقم الجوال']
    else:
        text_data = ['Phone Number']
    major = message.text
    bot.send_message(message.chat.id, f"{text_data[0]}:")
    bot.register_next_step_handler(message, welcome_message, name, major)


def welcome_message(message, name, major):
    # Access the user's input from the previous steps
    if lang[0] == 'ar':
        welcome_message_ = "شكرا على تسجيل معلوماتك سيتم التواصل معك من قبل احد ممثلي الخدمة"
    else:
        welcome_message_ = "Thank you for registering with us. We will get back to you soon."

    phone_number = message.text
    print(f"Name: {name}\nMajor: {major}\nPhone Number: {phone_number}")

    # Print the details
    # current date and time dd-mm-YY H:M:S
    current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    details = f"Your DETAILS:\n\nName: {name}\nMajor: {major}\nPhone Number: {phone_number} \n\n Date and Time: {current_date_time}"
    bot.send_message(message.chat.id, details)

    # Save the details in a csv file
    with open('queries.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([name, major, phone_number, current_date_time])

    bot.send_message(message.chat.id, welcome_message_)


@bot.message_handler(commands=['admin'])
def admin(message):
    df = pd.read_csv('queries.csv')
    df = df.to_string(index=False)
    bot.send_message(message.chat.id, df)


print("Bot is running...")
bot.polling()
