# A file that will store digest branch keyboards
# Import downloaded packages
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

update_channels_inline_button = InlineKeyboardButton(text="Update channel list", callback_data="update_channel")

approve_inline_button = InlineKeyboardButton(text="Approve", callback_data="digest_approve")
edit_inline_button = InlineKeyboardButton(text="Edit", callback_data="digest_edit")
cancel_inline_button = InlineKeyboardButton(text="Cancel", callback_data="digest_cancel")
regenerate_inline_button = InlineKeyboardButton(text="Regenerate", callback_data="digest_regenerate")
cancel_editing_inline_button = InlineKeyboardButton(text="Cancel editing", callback_data="cancel_editing")

digest_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [approve_inline_button],
    [edit_inline_button],
    [cancel_inline_button],
    [regenerate_inline_button]
])


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
