# A file that will store settings branch keyboards
# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

settings_back_inline_button = InlineKeyboardButton(text="Return back", callback_data="settings_back")
change_bot_language_inline_button = InlineKeyboardButton(text="Change bot language",
                                                         callback_data="change_bot_language")
change_api_key_inline_button = InlineKeyboardButton(text="Change LLM API key", callback_data="change_llm_api_key")

settings_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [settings_back_inline_button],
    [change_bot_language_inline_button],
    [change_api_key_inline_button]
])


def get_supported_bot_languages():
    # Get some data from database
    pass


def get_supported_llms():
    # Get some data from database
    pass
