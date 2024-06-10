from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import CHANNEL_ID
from utils.botUtils import getMessagesLastWeek

generate_router = Router()


@generate_router.message(Command('generate'))
async def get_posts(message: Message):
    await message.reply(str(getMessagesLastWeek(CHANNEL_ID)))
