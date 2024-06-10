from aiogram import Router
from aiogram.types import Message

from utils.databaseUtils import putMessage

channel_messages_router = Router()


@channel_messages_router.channel_post()
async def get_post(message: Message):
    putMessage(message, message.chat.id)
