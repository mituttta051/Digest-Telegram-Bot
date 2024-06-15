# A file that will store digest branch keyboards
# A file that will store digest branch keyboards
# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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