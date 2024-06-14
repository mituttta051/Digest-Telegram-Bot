from datetime import datetime

from create_bot import bot
from utils.databaseUtils import get_messages, get_channels


def get_period_in_seconds(date):
    return (datetime.now() - datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")).total_seconds()


def get_messages_last_week(channel_id):
    return list(filter(lambda x: get_period_in_seconds(x[1]) / 3600 / 24 <= 7, get_messages(channel_id)))


async def get_channels_with_permissions(user_id):
    return [(channel_id, name) for (_, channel_id, name) in get_channels() if user_id in list(map(lambda x: x.user.id, await bot.get_chat_administrators(channel_id)))]
