from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def channels_keyboard(channels):
    channels_kb_list = [
        [InlineKeyboardButton(text=name, callback_data=str(channel_id))] for (channel_id, name) in channels
    ]
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)


def generate_keyboard():
    keyboard = kb = [
        [KeyboardButton(text="Generate")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
