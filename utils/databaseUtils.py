from datetime import datetime

from aiogram.types import Message

from create_bot import cur, conn


def getAllMessages(id):
    table = "messages" + str(id).replace("-", "_")
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, text TEXT)""")
    cur.execute(f"""SELECT * FROM {table}""")
    return cur.fetchall()


def putMessage(message: Message, id):
    table = "messages" + str(id).replace("-", "_")
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, text TEXT)""")
    cur.execute(f"""INSERT INTO {table} (date, text) VALUES (?, ?)""", (datetime.now(), message.text))
    conn.commit()