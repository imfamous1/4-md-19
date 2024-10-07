from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot_settings import bot
from database import sqlite
from dotenv import load_dotenv
import os
import json

load_dotenv()
ADMIN = json.loads(os.getenv('ADMIN'))

def start_file_handler():
    # –––––– COMMANDS ------
    bot.register_message_handler(welcome_message, commands=['start'])
    # –––––– REGEXP ------

    # –––––– CALLBACKS ------



def welcome_message(message):
    try:
        sqlite.insert_user(message.from_user.id)

        bot.send_message(message.from_user.id, "Добро пожаловать в интернет-магазин товаров! "
                                               "Воспользуйтесь кнопками ниже для навигации.",
                         reply_markup=main_keyboard(message))
    except Exception as e:
        print(str(e))


def main_keyboard(message):
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton(text="📦Товары"), KeyboardButton(text="Инструкция"),
               KeyboardButton(text="Поддержка"))
    if message.from_user.id in ADMIN:
        markup.add(KeyboardButton(text="🛠Админ панель"))
    return markup



