# Import built-in packages
from datetime import datetime

# Import downloaded packages
from aiogram.types import Message
import psycopg2

conn = None
cur = None

# Init database
def init_db() -> None:
    global conn, cur
    conn = psycopg2.connect(dbname='digest-db', user='admin', password='secret', host='digest-db')
    cur = conn.cursor()
    create_tables()


# Create tables "users" and "channels" if they are not exist
def create_tables() -> None:
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS users (user_id TEXT PRIMARY KEY, language TEXT)"""
    )
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS channels (channel_id TEXT PRIMARY KEY, name TEXT, main_language TEXT, additional_language TEXT)"""
    )
    conn.commit()


# Define a function to retrieve messages from a specific channel
def get_messages(channel_id: str) -> list:
    table = "messages" + channel_id.replace("-", "_")
    cur.execute(f"""SELECT * FROM {table}""")
    return cur.fetchall()


# Define a function to store a message in a specific channel's table
def put_message(message: Message, channel_id: str) -> None:
    base_url = "https://t.me/"
    chat_id = message.chat.id
    message_id = message.message_id
    table = "messages" + str(channel_id).replace("-", "_")
    message_url = f"{base_url}c/{str(chat_id)[4:]}/{message_id}"
    cur.execute(f"""INSERT INTO {table} (date, text, link) VALUES (%s, %s, %s)""",
                (datetime.now(), message.html_text, message_url))
    conn.commit()


# Define a function to store a channel in the database or update its name if it already exists
def put_channel(channel_id: str, name: str) -> None:
    table = "messages" + str(channel_id).replace("-", "_")
    cur.execute(
        f"""INSERT INTO channels (channel_id, name, main_language, additional_language) VALUES (%s, %s, 'en', 'no') ON CONFLICT(channel_id) DO UPDATE SET name = EXCLUDED.name""",
        (str(channel_id), name))
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {table} (id SERIAL PRIMARY KEY, date TEXT, text TEXT, link TEXT)""")
    conn.commit()


# Define a function to retrieve all channels from the database
def get_channels() -> list:
    cur.execute(f"""SELECT * FROM channels""")
    return cur.fetchall()

def get_main_language(channel_id):
    cur.execute("SELECT main_language FROM channels WHERE channel_id = %s", (str(channel_id),))
    return cur.fetchone()[0]


def get_additional_language(channel_id):
    cur.execute("SELECT additional_language FROM channels WHERE channel_id = %s", (str(channel_id),))
    return cur.fetchone()[0]

def update_main_language(channel_id, new_language):
    cur.execute("UPDATE channels SET main_language = %s WHERE channel_id = %s", (new_language, str(channel_id)))
    conn.commit()

def update_additional_language(channel_id, new_language):
    cur.execute("UPDATE channels SET additional_language = %s WHERE channel_id = %s", (new_language, str(channel_id)))
    conn.commit()


def put_user(user_id):
    cur.execute(
        f"""INSERT INTO users (user_id, language) VALUES (%s, 'en') ON CONFLICT (user_id) DO NOTHING""",
        (str(user_id),))
    conn.commit()

def get_bot_language_db(user_id):
    if user_id is None:
        return "en"
    cur.execute("SELECT language FROM users WHERE user_id = %s", (str(user_id),))
    return cur.fetchone()[0]

def update_bot_language(user_id, new_language):
    if user_id is None:
        return
    cur.execute("UPDATE users SET language = %s WHERE user_id = %s", (new_language, str(user_id)))
    conn.commit()