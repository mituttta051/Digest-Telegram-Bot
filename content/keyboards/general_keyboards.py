# A file that will store the general keyboards
# Or keyboards that doesn't belong to branches

# Import downloaded packages
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

# Start menu
start_reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Create digest"), KeyboardButton(text="Settings")],
    [KeyboardButton(text="Help")]
],
    resize_keyboard=True,
    input_field_placeholder="Select a menu button",
    one_time_keyboard=True
)


def make_inline_keyboard(*buttons: InlineKeyboardButton) -> InlineKeyboardMarkup:
    inline_keyboard = []
    for button in buttons:
        inline_keyboard.append([button])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def one_button_keyboard(button_type: str, text: str) -> ReplyKeyboardMarkup | InlineKeyboardMarkup:
    if button_type.lower() == "reply":
        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text)]], resize_keyboard=True, one_time_keyboard=True)
    elif button_type.lower() == "inline":
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, callback_data="empty-data")]])
