# A file that will contain various technical functions
import logging
# Import downloaded packages
from datetime import datetime

# Import project files
from create_bot import bot, logger
from utils.databaseUtils import get_messages, get_channels


# Define a function to calculate the period in seconds between the current time and a given date
def get_period_in_seconds(date: str) -> float:
    """
    Function to calculate the period in seconds between the current time and a given date.

    This function takes a date string in the format "%Y-%m-%d %H:%M:%S.%f" and calculates the difference in seconds
    between that date and the current time.

    Args:
        date (str): The date string in the format "%Y-%m-%d %H:%M:%S.%f".

    Returns:
        float: The period in seconds between the current time and the given date.
    """
    return (datetime.now() - datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")).total_seconds()


# Define a function to retrieve messages from the last week for a given channel
def get_messages_last_week(channel_id: str) -> list[str]:
    """
    Function to retrieve messages from the last week for a given channel.

    This function queries the database for messages from the specified channel and filters them to include only those
    that were posted within the last week.

    Args:
        channel_id (str): The ID of the channel to retrieve messages from.

    Returns:
        list[str]: A list of messages posted within the last week.
    """
    return list(filter(lambda x: get_period_in_seconds(x[1]) / 3600 / 24 <= 7, get_messages(channel_id)))


# Define a function to retrieve messages within a specified number of days for a given channel
def get_messages_in_days(channel_id: str, period: str) -> list[str]:
    """
    Function to retrieve messages within a specified number of days for a given channel.

    This function queries the database for messages from the specified channel and filters them to include only those
    that were posted within the specified number of days.

    Args:
        channel_id (str): The ID of the channel to retrieve messages from.
        period (str): The number of days to consider for message retrieval.

    Returns:
        list[str]: A list of messages posted within the specified number of days.
    """
    return list(filter(lambda x: get_period_in_seconds(x[1]) / 3600 / 24 <= int(period), get_messages(channel_id)))


# Define an asynchronous function to retrieve channels with permissions for a given user
async def get_channels_with_permissions(user_id: int) -> list[(str, str)]:
    """
    Asynchronous function to retrieve channels with permissions for a given user.

    This function queries the database for channels and checks if the user with the specified ID is an administrator
    in those channels. It returns a list of tuples, where each tuple contains the channel ID and name for channels
    where the user has administrator permissions.

    Args:
        user_id (int): The ID of the user to check for channel permissions.

    Returns:
        list[(str, str)]: A list of tuples, where each tuple contains the channel ID and name for channels where the
        user has administrator permissions.
    """
    result = []
    for _, channel_id, name in get_channels():
        try:
            if user_id in list(map(lambda x: x.user.id, await bot.get_chat_administrators(channel_id))):
                result.append((channel_id, name))
        except:
            logger.exception(f"Bot not in the channel: {channel_id}")
    return result


def attach_link_to_message(message: str, link: str):
    message = "a ofuclio vov"
    if message.find("—") != -1 and message.find("-") != -1:
        index = min(message.find("—"), message.find("-"))
    else:
        index = max(message.find("—"), message.find("-"))

    if index != -1:
        message = "<a href=\"{0}\">{1}</a>".format(link, message[:index]) + message[index:]
    else:
        words = message.split()
        message = ""
        found = False
        for word in words:
            if len(word) > 2 and not found:
                message += " " + "<a href=\"{0}\">{1}</a>".format(link, word)
                found = True
                continue
            message += " " + word
    return message