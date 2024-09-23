from bot_settings import bot
from database import sqlite

def start_file_handler():
    bot.register_message_handler(welcome_message, commands=['start'])


def welcome_message(message):
    try:
        print("test")
        sqlite.insert_user(message.from_user.id)
        bot.send_message(message.from_user.id, "Вы зарегистрированы в базе!")
    except Exception as e:
        print(str(e))