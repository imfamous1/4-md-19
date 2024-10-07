import sqlite3

connection = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = connection.cursor()


def insert_user(user_id):
    with connection as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT user_id from subscriptions where user_id = ?', (user_id, ))
        user = cursor.fetchone()
        if user is None:
            cursor.execute('INSERT INTO subscriptions (user_id) values (?)', (user_id,))
        else:
            print("Пользователь уже есть в базе!")


def get_products_category():
    with connection as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT category FROM products').fetchall()
        return result


def get_products_info_by_category(category):
    with connection as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT id, product_name, product_quantity, price FROM products WHERE category = ?',
                                (category, )).fetchall()
        return result


def get_bot_users():
    with connection as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT id, user_id FROM subscriptions').fetchall()
        return result


def get_users_id():
    with connection as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT user_id FROM subscriptions').fetchall()
        return result


def get_product_description_by_id(id):
    with connection as conn:
        cursor = conn.cursor()
        result = cursor.execute('SELECT description, photo FROM products WHERE id = ?',
                                (id, )).fetchone()
        return result