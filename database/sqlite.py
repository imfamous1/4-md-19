import sqlite3

connection = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = connection.cursor()


def insert_user(user_id):
    with connection as conn:
        conn.cursor().execute('INSERT INTO subscriptions (user_id) values (?)', (user_id,))
