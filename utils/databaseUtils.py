from datetime import datetime

from aiogram.types import Message

from create_bot import cur, conn


def get_messages(channel_id):
    table = "messages" + str(channel_id).replace("-", "_")
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, text TEXT)""")
    cur.execute(f"""SELECT * FROM {table}""")
    return cur.fetchall()


def put_message(message: Message, channel_id):
    table = "messages" + str(channel_id).replace("-", "_")
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, text TEXT)""")
    cur.execute(f"""INSERT INTO {table} (date, text) VALUES (?, ?)""", (datetime.now(), message.html_text))
    conn.commit()


def put_channel(channel_id, name):
    cur.execute(f"""INSERT INTO channels (channel_id, name) VALUES (?, ?) ON CONFLICT(channel_id) DO UPDATE SET name = ?""", (channel_id, name, name))
    conn.commit()


def get_channels():
    cur.execute(f"""SELECT * FROM channels""")
    return cur.fetchall()
