from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from utils.botUtils import getMessagesLastWeek

generate_router = Router()


@generate_router.message(Command('generate'))
async def get_posts(message: Message):
    await message.reply(str(getMessagesLastWeek(message.text.lstrip("/generate ").lstrip())))
