import telebot
from bot_settings import bot
from handlers import start_file


def register_handlers():
    start_file.start_file_handler()


register_handlers()

bot.polling(none_stop=True)