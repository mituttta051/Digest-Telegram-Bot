# A file that will store settings branch keyboards

# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

return_back_inline_button = InlineKeyboardButton(text="⬅️Back", callback_data="back")

# Define reply keyboard buttons for settings actions
return_back_reply_button = KeyboardButton(text="⬅️Back")
change_bot_language_reply_button = KeyboardButton(text="🌍Bot language")
channel_settings_key_reply_button = KeyboardButton(text="⚙️Channel settings")

# Define inline keyboard buttons for settings actions
ru_language_button = InlineKeyboardButton(text="🇷🇺Russian", callback_data="ru")
en_language_button = InlineKeyboardButton(text="🇬🇧English", callback_data="en")

# Define inline keyboard buttons for channel settings actions
api_button = InlineKeyboardButton(text="🛠API", callback_data="api")
main_language_button = InlineKeyboardButton(text="🌍Main language", callback_data="main_language")
addition_language_button = InlineKeyboardButton(text="🌎Addition language", callback_data="addition_language")

# Create a reply keyboard for settings actions
settings_reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [change_bot_language_reply_button, channel_settings_key_reply_button],
    [return_back_reply_button]
],
    resize_keyboard=True,
    input_field_placeholder="Select a menu button",
    one_time_keyboard=True
)

# Create an inline keyboard for choosing language
settings_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [ru_language_button],
    [en_language_button],
    [return_back_inline_button]
])

channel_settings_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [api_button],
    [main_language_button],
    [addition_language_button],
    [return_back_inline_button]
])

digest_languages = ["🇷🇺Russian", "🇬🇧English"]
digest_addition_languages = ["🇷🇺Russian", "🇬🇧English", "❌Cancel"]

def digest_bot_languages_keyboard():
    channels_kb_list = [
        [InlineKeyboardButton(text=language, callback_data=language)] for language in digest_languages
    ]
    channels_kb_list.append([return_back_inline_button])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)

def digest_bot_addition_languages_keyboard():
    channels_kb_list = [
        [InlineKeyboardButton(text=language, callback_data=language)] for language in digest_addition_languages
    ]
    channels_kb_list.append([return_back_inline_button])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)
