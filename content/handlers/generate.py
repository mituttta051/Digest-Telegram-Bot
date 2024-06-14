from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from content.keyboards.generate_keyboards import channels_keyboard
from utils.botUtils import get_messages_last_week, get_channels_with_permissions

generate_router = Router()


@generate_router.message(Command('generate'))
async def get_posts(message: Message):
    channels = await get_channels_with_permissions(message.chat.id)
    await message.answer("Choose a channel", reply_markup=channels_keyboard(channels))


@generate_router.callback_query()
async def generate_callback_query(call: CallbackQuery):
    await call.message.answer(str(get_messages_last_week(int(call.data))))
