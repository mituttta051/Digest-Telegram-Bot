# A file that will store settings branch keyboards
# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

settings_back_inline_button = InlineKeyboardButton(text="Return back", callback_data="settings_back")

settings_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [settings_back_inline_button]
])
