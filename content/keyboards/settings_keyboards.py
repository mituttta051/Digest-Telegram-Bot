# A file that will store settings branch keyboards

# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Define inline keyboard buttons for settings actions
settings_back_inline_button = InlineKeyboardButton(text="Return back", callback_data="settings_back")
change_bot_language_inline_button = InlineKeyboardButton(text="Change bot language", callback_data="change_bot_language")
change_api_key_inline_button = InlineKeyboardButton(text="Change LLM API key", callback_data="change_llm_api_key")

# Create an inline keyboard for settings actions
settings_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [settings_back_inline_button],
    [change_bot_language_inline_button],
    [change_api_key_inline_button]
])


# Define a function to retrieve supported bot languages from the database
def get_supported_bot_languages():
    """
    Function to retrieve a list of supported bot languages from the database.

    This function is intended to query the database and return a list of languages that the bot can operate in.
    However, the implementation is currently a placeholder and does not perform any actual database operations.

    Returns:
        list: A list of supported bot languages.
    """
    # Get some data from database
    pass


# Define a function to retrieve supported LLMs (Language Models) from the database
def get_supported_llms():
    """
    Function to retrieve a list of supported LLMs (Language Models) from the database.

    This function is intended to query the database and return a list of language models that the bot can use for
    generating responses. However, the implementation is currently a placeholder and does not perform any actual
    database operations.

    Returns:
        list: A list of supported LLMs.
    """
    # Get some data from database
    pass
