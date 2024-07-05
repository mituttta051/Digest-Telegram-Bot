# A file that will store digest branch keyboards

# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from resources.translation_dictionary import localise
from utils.botUtils import get_bot_language
from content.handlers.settings_handlers import SettingsFSM

# Return back button

return_back_button = InlineKeyboardButton(text=localise("⬅️Back", get_bot_language(SettingsFSM.selected_bot_language)), callback_data="back")

# Buttons to choose digest period
week_period_inline_button = InlineKeyboardButton(text=localise("Week (7 days)", get_bot_language(SettingsFSM.selected_bot_language)) , callback_data="7")
two_weeks_period_inline_button = InlineKeyboardButton(text=localise("2 weeks (14 days)", get_bot_language(SettingsFSM.selected_bot_language)), callback_data="14")
month_period_inline_button = InlineKeyboardButton(text=localise("1 Month (30 days)", get_bot_language(SettingsFSM.selected_bot_language)), callback_data="30")

# Buttons connected with digest activity
approve_inline_button = InlineKeyboardButton(text=localise("✅Approve", get_bot_language(SettingsFSM.selected_bot_language)), callback_data="digest_approve")
edit_inline_button = InlineKeyboardButton(text=localise("✏️Edit", get_bot_language(SettingsFSM.selected_bot_language)), callback_data="digest_edit")
cancel_inline_button = InlineKeyboardButton(text=localise("❌Cancel", get_bot_language(SettingsFSM.selected_bot_language)), callback_data="digest_cancel")
regenerate_inline_button = InlineKeyboardButton(text=localise("🔄Regenerate", get_bot_language(SettingsFSM.selected_bot_language)), callback_data="digest_regenerate")
cancel_editing_inline_button = InlineKeyboardButton(text=localise("❌Cancel editing", get_bot_language(SettingsFSM.selected_bot_language)), callback_data="cancel_editing")

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
