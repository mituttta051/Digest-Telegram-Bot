# A file that will store digest branch keyboards

# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Return back button

return_back_button = InlineKeyboardButton(text="⬅️Back", callback_data="back")

# Buttons to choose digest period
week_period_inline_button = InlineKeyboardButton(text="Week (7 days)", callback_data="7")
two_weeks_period_inline_button = InlineKeyboardButton(text="2 weeks (14 days)", callback_data="14")
month_period_inline_button = InlineKeyboardButton(text="1 Month (30 days)", callback_data="30")

# Buttons connected with digest activity
approve_inline_button = InlineKeyboardButton(text="✅Approve", callback_data="digest_approve")
edit_inline_button = InlineKeyboardButton(text="✏️Edit", callback_data="digest_edit")
cancel_inline_button = InlineKeyboardButton(text="❌Cancel", callback_data="digest_cancel")
regenerate_inline_button = InlineKeyboardButton(text="🔄Regenerate", callback_data="digest_regenerate")
cancel_editing_inline_button = InlineKeyboardButton(text="❌Cancel editing", callback_data="cancel_editing")

# Create an inline keyboard for digest actions
digest_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [approve_inline_button],
    [edit_inline_button],
    [cancel_inline_button],
    [regenerate_inline_button]
])

# Create an inline keyboard for supported period selection
supported_period_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [week_period_inline_button],
    [two_weeks_period_inline_button],
    [month_period_inline_button],
    [return_back_button]
])
