# A file that will contain general message, command and callback handlers from settings branch

# Import downloaded packages
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

# Import project files
from content.handlers.general_handlers import bot_start
import content.keyboards.settings_keyboards as sk

settings_router = Router()


@settings_router.message(F.text == "Settings")
async def bot_settings(message: Message):
    await message.answer("Welcome to the settings!", reply_markup=sk.settings_inline_keyboard)


@settings_router.callback_query(F.data == "settings_back")
async def settings_back(callback: CallbackQuery):
    await callback.answer('You chose "Return back"')
    await bot_start(callback.message)
