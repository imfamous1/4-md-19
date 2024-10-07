from bot_settings import bot
from handlers import start_message, products, admin


def register_handlers():
    start_message.start_file_handler()
    products.products_handler()
    admin.admin_handler()


register_handlers()

bot.polling(none_stop=True)