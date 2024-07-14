# Import built-in packages
from datetime import datetime

# Import downloaded packages
from aiogram.types import Message

from content.FSMs.settings_FSMs import SettingsFSM
# Import project files
from create_bot import cur, conn


# Define a function to retrieve messages from a specific channel
def get_messages(channel_id: str) -> list:
    """
    Function to retrieve all messages from a specific channel.

    This function constructs a table name based on the channel ID, ensuring that each channel has its own table. It then
    executes a SQL query to select all records from the specified table and returns the result as a list of tuples.

    Args:
        channel_id (str): The ID of the channel to retrieve messages from.

    Returns:
        list: A list of tuples representing the messages from the specified channel.
    """
    table = "messages" + channel_id.replace("-", "_")
    cur.execute(f"""SELECT * FROM {table}""")
    return cur.fetchall()


# Define a function to store a message in a specific channel's table
def put_message(message: Message, channel_id: str) -> None:
    """
    Function to store a message in a specific channel's table.

    This function constructs a table name based on the channel ID and inserts a new record into the table with the
    current date and the HTML-formatted text of the message.

    Args:
        message (Message): The Telegram message object to store.
        channel_id (str): The ID of the channel to store the message in.
    """
    # to retrieve message link
    base_url = "https://t.me/"
    chat_id = message.chat.id
    message_id = message.message_id
    table = "messages" + str(channel_id).replace("-", "_")
    message_url = f"{base_url}c/{str(chat_id)[4:]}/{message_id}"
    cur.execute(f"""INSERT INTO {table} (date, text, link) VALUES (?, ?, ?)""",
                (datetime.now(), message.html_text, message_url))
    conn.commit()


# Define a function to store a channel in the database or update its name if it already exists
def put_channel(channel_id: str, name: str) -> None:
    """
    Function to store a channel in the database or update its name if it already exists.

    This function inserts a new record into the 'channels' table with the channel ID and name. If a record with the same
    channel ID already exists, it updates the name of the existing record. Additionally, it creates a new table for the
    channel's messages if it does not already exist.

    Args:
        channel_id (str): The ID of the channel to store or update.
        name (str): The name of the channel.
    """
    table = "messages" + str(channel_id).replace("-", "_")
    cur.execute(
        f"""INSERT INTO channels (channel_id, name, main_language, additional_language) VALUES (?, ?, 'en', 'no') ON CONFLICT(channel_id) DO UPDATE SET name = ?""",
        (channel_id, name, name))
    cur.execute(
        f"""CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, text TEXT, link TEXT)""")
    conn.commit()


# Define a function to retrieve all channels from the database
def get_channels() -> list:
    """
    Function to retrieve all channels from the database.

    This function executes a SQL query to select all records from the 'channels' table and returns the result as a list
    of tuples.

    Returns:
        list: A list of tuples representing the channels in the database.
    """
    cur.execute(f"""SELECT * FROM channels""")
    return cur.fetchall()


def get_main_language(channel_id):
    cur.execute("SELECT main_language FROM channels WHERE channel_id = ?", (channel_id,))
    return cur.fetchone()[0]


def get_additional_language(channel_id):
    cur.execute("SELECT additional_language FROM channels WHERE channel_id = ?", (channel_id,))
    return cur.fetchone()[0]


def update_main_language(channel_id, new_language):
    cur.execute("UPDATE channels SET main_language = ? WHERE channel_id = ?", (new_language, channel_id))
    conn.commit()


def update_additional_language(channel_id, new_language):
    cur.execute("UPDATE channels SET additional_language = ? WHERE channel_id = ?", (new_language, channel_id))
    conn.commit()


def put_user(user_id):
    cur.execute(
        f"""INSERT OR IGNORE INTO users (user_id, language) VALUES (?, 'en')""",
        (user_id,))
    conn.commit()


def get_bot_language_db(user_id):
    if user_id is None:
        return "en"
    cur.execute("SELECT language FROM users WHERE user_id = ?", (user_id,))
    return cur.fetchone()[0]


def update_bot_language(user_id, new_language):
    if user_id is None:
        return
    cur.execute("UPDATE users SET language = ? WHERE user_id = ?", (new_language, user_id))
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
    cur.execute("UPDATE channels SET auto_digest = ? WHERE channel_id = ?", (option, channel_id))
    conn.commit()


def change_auto_digest_date(channel_id, date):
    if channel_id is None:
        return
    cur.execute("UPDATE channels SET auto_digest_date = ? WHERE channel_id = ?", (date, channel_id))
    conn.commit()


def get_auto_digest_data(channel_id):
    if channel_id is None:
        return "no"
    cur.execute("SELECT auto_digest, auto_digest_date FROM channels WHERE channel_id = ?", (channel_id,))
    return cur.fetchone()


def get_api_key(channel_id):
    cur.execute("SELECT api_key FROM channels WHERE channel_id = ?", (channel_id,))
    return cur.fetchone()[0]


def get_folder_id(channel_id):
    cur.execute("SELECT folder_id FROM channels WHERE channel_id = ?", (channel_id,))
    return cur.fetchone()[0]


def update_api_key(channel_id, api_key):
    cur.execute("UPDATE channels SET api_key = ? WHERE channel_id = ?", (api_key, channel_id))
    conn.commit()


def update_folder_id(channel_id, folder_id):
    cur.execute("UPDATE channels SET folder_id = ? WHERE channel_id = ?", (folder_id, channel_id))
    conn.commit()
