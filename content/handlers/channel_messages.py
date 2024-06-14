from aiogram import Router
from aiogram.types import Message

from utils.databaseUtils import put_message, put_channel

channel_messages_router = Router()


@channel_messages_router.channel_post()
async def get_post(message: Message):
    put_channel(message.chat.id, message.chat.title)
    put_message(message, message.chat.id)
