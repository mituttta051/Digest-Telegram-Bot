from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from content.keyboards.generate_keyboards import generate_keyboard
from create_bot import bot
from utils.botUtils import get_channels_with_permissions

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Click generate to generate summary", reply_markup=generate_keyboard())


@start_router.message(F.text == "/test")
async def cmd_start(message: Message):
    channels = await get_channels_with_permissions(message.chat.id)
    await message.answer(str(channels))

