from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define inline keyboard buttons
return_back_button = InlineKeyboardButton(text="⬅️Back", callback_data="back")
week_period_inline_button = InlineKeyboardButton(text="Week (7 days)", callback_data="7")
two_weeks_period_inline_button = InlineKeyboardButton(text="2 weeks (14 days)", callback_data="14")
month_period_inline_button = InlineKeyboardButton(text="1 Month (30 days)", callback_data="30")
custom_period_inline_button = InlineKeyboardButton(text="Custom period", callback_data="custom_period")

approve_inline_button = InlineKeyboardButton(text="✅Approve", callback_data="digest_approve")
edit_inline_button = InlineKeyboardButton(text="✏️Edit", callback_data="digest_edit")
cancel_inline_button = InlineKeyboardButton(text="❌Cancel", callback_data="digest_cancel")
regenerate_inline_button = InlineKeyboardButton(text="🔄Regenerate", callback_data="digest_regenerate")
cancel_editing_inline_button = InlineKeyboardButton(text="❌Cancel editing", callback_data="cancel_editing")

# Create inline keyboards
digest_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [approve_inline_button],
    [edit_inline_button],
    [cancel_inline_button],
    [regenerate_inline_button]
])

supported_period_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [week_period_inline_button],
    [two_weeks_period_inline_button],
    [month_period_inline_button],
    [custom_period_inline_button],
    [return_back_button]
])

return_back_button_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [return_back_button]
])
