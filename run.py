from bot_settings import bot
from handlers import start_file, products


def register_handlers():
    start_file.start_file_handler()
    products.products_handler()

register_handlers()

bot.polling(none_stop=True)