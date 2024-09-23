from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot_settings import bot
from database import sqlite

def start_file_handler():
    # –––––– COMMANDS ------
    bot.register_message_handler(welcome_message, commands=['start'])
    # –––––– REGEXP ------

    # –––––– CALLBACKS ------



def welcome_message(message):
    try:
        sqlite.insert_user(message.from_user.id)

        bot.send_message(message.from_user.id, "Добро пожаловать в интернет-магазин товаров! "
                                               "Воспользуйтесь кнопками ниже для навигации.", reply_markup=main_keyboard())
    except Exception as e:
        print(str(e))


def main_keyboard():
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton(text="📦Товары"), KeyboardButton(text="Инструкция"),
               KeyboardButton(text="Поддержка"))
    return markup



