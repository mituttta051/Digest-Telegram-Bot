from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from content.keyboards.digest_keyboards import channels_keyboard
from utils.LLMUtils import generate_summary
from utils.botUtils import get_messages_last_week, get_channels_with_permissions

generate_router = Router()


@generate_router.message(F.text == "Generate")
async def get_posts(message: Message):
    channels = await get_channels_with_permissions(message.chat.id)
    await message.answer("Choose a channel", reply_markup=channels_keyboard(channels))


@generate_router.callback_query()
async def generate_callback_query(call: CallbackQuery):
    channels = await get_channels_with_permissions(call.message.chat.id)
    messages = get_messages_last_week(int(call.data))
    if len(messages) == 0:
        await call.message.answer("С момента добавления бота не было выложено ни одного поста",
                                  reply_markup=channels_keyboard(channels))
    else:
        await call.message.answer(await generate_summary(get_messages_last_week(int(call.data))),
                                  reply_markup=channels_keyboard(channels))
