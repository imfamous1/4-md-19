from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputMedia
from bot_settings import bot
from database import sqlite

def products_handler():
    # –––––– COMMANDS ------

    # –––––– REGEXP ------
    bot.register_message_handler(send_products_to_user_message, regexp="📦Товары")
    bot.register_message_handler(send_support_message, regexp="Поддержка")
    bot.register_message_handler(send_instruction, regexp="Инструкция")
    # –––––– CALLBACKS ------
    bot.register_callback_query_handler(delete_message, lambda x: x.data.startswith('delete_message'))
    bot.register_callback_query_handler(send_products_by_category, lambda x: x.data.startswith('category_'))
    bot.register_callback_query_handler(send_products_to_user_message_edit,
                                        lambda x: x.data.startswith('back_to_category'))
    bot.register_callback_query_handler(send_product_description,
                                        lambda x: x.data.startswith('send_product_description_'))



def send_products_to_user_message_edit(call):
    send_products_to_user_message(call, edit=True)


def send_products_to_user_message(message, edit=False):
    categories = sqlite.get_products_category()
    unique_categories = set([item[0] for item in categories])
    markup = InlineKeyboardMarkup()
    for categories in unique_categories:
        markup.add(InlineKeyboardButton(text=f"{categories}", callback_data=f'category_{categories}'))
    markup.add(InlineKeyboardButton(text="Назад", callback_data='delete_message'))
    caption = "Выберите категорию товаров:"
    with open(f'images/00.jpg', 'rb') as img:
        if not edit:
            try:
                bot.send_photo(message.from_user.id, img, caption, reply_markup=markup)
            except Exception as e:
                print(str(e))
        else:
            media = InputMedia(type='photo', media=img)
            bot.edit_message_media(chat_id=message.message.chat.id, message_id=message.message.message_id, media=media)
            bot.edit_message_caption(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                     caption=caption)
            bot.edit_message_reply_markup(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                          reply_markup=markup)


def send_products_by_category(call):
    category = call.data[9:]
    products = sqlite.get_products_info_by_category(category)
    markup = InlineKeyboardMarkup()
    for item in products:
        markup.add(InlineKeyboardButton(text=f"{item[1]}, {item[2]}, {item[3]}",
                                        callback_data=f"send_product_description_{item[0]}"))
    markup.add(InlineKeyboardButton(text="Назад", callback_data="back_to_category"))
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=markup)



def send_product_description(call):
    product_id = call.data[25:]
    description, photo = sqlite.get_product_description_by_id(product_id)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Назад", callback_data='back_to_category'))
    if description is None:
        description = "Нет описания товара"
    try:
        with open(f'{photo}', 'rb') as img:
            media = InputMedia(type='photo', media=img)
            bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id, media=media)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=description)
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          reply_markup=markup)
    except Exception as e:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=description)
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      reply_markup=markup)


def delete_message(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def send_support_message(message):
    link = '[Написать менеджеру](https://t.me/zkokorin)'
    bot.send_message(message.from_user.id, link, parse_mode='markdown')


def send_instruction(message):
    try:
        link = '[Прочитать инструкцию](https://telegra.ph/Instrukciya-10-07-14)'
        bot.send_message(message.from_user.id, link, parse_mode='markdown')
    except Exception as e:
        bot.send_message(message.from_user.id, "Кнопка сломалась, попробуйте позже!")