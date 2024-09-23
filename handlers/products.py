from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from bot_settings import bot
from database import sqlite

def products_handler():
    # –––––– COMMANDS ------

    # –––––– REGEXP ------
    bot.register_message_handler(send_products_to_user_message, regexp="📦Товары")
    bot.register_message_handler(send_support_message, regexp="Поддержка")
    # –––––– CALLBACKS ------
    bot.register_callback_query_handler(delete_message, lambda x: x.data.startswith('delete_message'))
    bot.register_callback_query_handler(send_products_by_category, lambda x: x.data.startswith('category_'))
    bot.register_callback_query_handler(send_products_to_user_message_edit, lambda x: x.data.startswith('back_to_category'))


def send_products_to_user_message_edit(call):
    send_products_to_user_message(call, edit=True)


def send_products_to_user_message(message, edit=False):
    categories = sqlite.get_products_category()
    unique_categories = set([item[0] for item in categories])
    markup = InlineKeyboardMarkup()
    for categories in unique_categories:
        markup.add(InlineKeyboardButton(text=f"{categories}", callback_data=f'category_{categories}'))
    markup.add(InlineKeyboardButton(text="Назад", callback_data='delete_message'))
    if not edit:
        try:
            with open(f'images/00.jpg', 'rb') as img:
                bot.send_photo(message.from_user.id, img, "Выберите категорию товаров:", reply_markup=markup)
        except Exception as e:
            print(str(e))
    else:
        bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                      reply_markup=markup)


def send_products_by_category(call):
    category = call.data[9:]
    products = sqlite.get_products_info_by_category(category)
    markup = InlineKeyboardMarkup()
    for item in products:
        markup.add(InlineKeyboardButton(text=f"{item[0]}, {item[1]}, {item[2]}", callback_data="test"))
    markup.add(InlineKeyboardButton(text="Назад", callback_data="back_to_category"))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)


def delete_message(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def send_support_message(message):
    link = '[Написать менеджеру](https://t.me/zkokorin)'
    bot.send_message(message.from_user.id, link, parse_mode='markdown')

