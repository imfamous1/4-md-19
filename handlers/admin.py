from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot_settings import bot
from dotenv import load_dotenv
from database import sqlite
import os
import json

load_dotenv()
ADMIN = json.loads(os.getenv('ADMIN'))


def admin_handler():
    # –––––– COMMANDS ------
    bot.register_message_handler(admin_message, commands=['admin'])
    # –––––– REGEXP ------
    bot.register_message_handler(admin_message, regexp="🛠Админ панель")
    # –––––– CALLBACKS ------
    bot.register_callback_query_handler(send_bot_users, lambda x: x.data.startswith('send_bot_users'))
    bot.register_callback_query_handler(send_message_to_users, lambda x: x.data.startswith('send_message_to_users'))
    bot.register_callback_query_handler(cancel_sending_message, lambda x: x.data.startswith('cancel_message'))


def admin_message(message):
    count = 10
    if message.from_user.id in ADMIN:
        caption = f"Это админская панель.\n\nКоличество пользователей бота: *{count}*"
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Пользователи бота", callback_data='send_bot_users'),
                   InlineKeyboardButton(text="Отправить сообщение", callback_data='send_message_to_users'))
        markup.add(InlineKeyboardButton(text="Назад", callback_data='delete_message'))
        bot.send_message(message.from_user.id, caption, reply_markup=markup, parse_mode='markdown')


def send_bot_users(call):
    if call.from_user.id in ADMIN:
        users = sqlite.get_bot_users()
        print(users)
        caption = ''
        for user in users:
            user_str = ') '.join(map(str, user))
            caption += f'{user_str}\n'
        try:
            bot.send_message(call.from_user.id, caption)
        except Exception as e:
            bot.send_message(call.from_user.id, "Слишком большое количество людей для сообщения.")


def send_message_to_users(call):
    if call.from_user.id in ADMIN:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Отменить отправку", callback_data='cancel_message'))
        msg = bot.send_message(call.from_user.id, "Введите текст для отправки рассылки:", reply_markup=markup)
        bot.register_next_step_handler(msg, process_message_for_users)


def process_message_for_users(message):
    if message.from_user.id in ADMIN:
        text_to_send = message.text
        users_id = sqlite.get_users_id()
        for user in users_id:
            bot.send_message(user[0], text_to_send)


def cancel_sending_message(call):
    if call.from_user.id in ADMIN:
        bot.clear_step_handler_by_chat_id(call.message.chat.id)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Отправка отменена!")