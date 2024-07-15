# Import built-in packages
from datetime import datetime

import psycopg2
# Import downloaded packages
from aiogram.types import Message

from content.FSMs.settings_FSMs import SettingsFSM

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

async def change_auto_digest(state):
    temp = await state.get_state()
    await state.set_state(SettingsFSM.data)
    data = await state.get_data()
    await state.set_state(temp)
    channel_id = data.get("channel_id", "0")
    switch = get_auto_digest_data(channel_id)[0]
    if switch == "no":
        switch = "yes"
    else:
        switch = "no"
    change_auto_digest_(channel_id, switch)


def change_auto_digest_(channel_id, option):
    if channel_id is None:
        return
    cur.execute("UPDATE channels SET auto_digest = %s WHERE channel_id = %s", (option, channel_id))
    conn.commit()

def change_auto_digest_date(channel_id, date):
    if channel_id is None:
        return
    cur.execute("UPDATE channels SET auto_digest_date = %s WHERE channel_id = %s", (date, channel_id))
    conn.commit()

def get_auto_digest_data(channel_id):
    if channel_id is None:
        return {"auto_digest": "no"}
    cur.execute("SELECT auto_digest, auto_digest_date FROM channels WHERE channel_id = %s", (channel_id,))
    result = cur.fetchone()
    return {"auto_digest": result[0], "auto_digest_date": result[1]} if result else {"auto_digest": "no"}

def get_api_key(channel_id):
    cur.execute("SELECT api_key FROM channels WHERE channel_id = %s", (channel_id,))
    result = cur.fetchone()
    return result[0] if result else None

def get_folder_id(channel_id):
    cur.execute("SELECT folder_id FROM channels WHERE channel_id = %s", (channel_id,))
    result = cur.fetchone()
    return result[0] if result else None

def update_api_key(channel_id, api_key):
    cur.execute("UPDATE channels SET api_key = %s WHERE channel_id = %s", (api_key, channel_id))
    conn.commit()

def update_folder_id(channel_id, folder_id):
    cur.execute("UPDATE channels SET folder_id = %s WHERE channel_id = %s", (folder_id, channel_id))
    conn.commit()
