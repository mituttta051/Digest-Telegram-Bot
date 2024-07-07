# A file that will store settings branch keyboards

# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from resources.locales.translation_dictionary import localise
from utils.botUtils import get_bot_language

# Define inline keyboard buttons for settings actions
ru_language_button = InlineKeyboardButton(text="🇷🇺Russian", callback_data="ru")
en_language_button = InlineKeyboardButton(text="🇬🇧English", callback_data="en")
# Define inline keyboard buttons for channel settings actions
api_button = InlineKeyboardButton(text="🛠API", callback_data="api")
main_language_button = InlineKeyboardButton(text="🌍Main language", callback_data="main_language")
addition_language_button = InlineKeyboardButton(text="🌎Addition language", callback_data="addition_language")

# Create a reply keyboard for settings actions
async def settings_reply_keyboard(state):
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=await localise("🌍Bot language", state)),
         KeyboardButton(text=await localise("⚙️Channel settings", state))],
        [KeyboardButton(text=await localise("⬅️Back", state))]
    ],
        resize_keyboard=True,
        input_field_placeholder=await localise("Select a menu button", state),
        one_time_keyboard=True
    )


async def channel_settings_inline_keyboard(state):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await localise("🛠API", state), callback_data="api")],
        [InlineKeyboardButton(text=await localise("🌍Main language", state), callback_data="main_language")],
        [InlineKeyboardButton(text=await localise("🌎Addition language", state),
                              callback_data="addition_language")],
        [InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")]
    ])


digest_languages = [("🇷🇺Russian", "ru"), ("🇬🇧English", "en")]


async def digest_bot_languages_keyboard(state):
    channels_kb_list = [
        [InlineKeyboardButton(text=language[0], callback_data=language[1])] for language in digest_languages
    ]
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)


# Create an inline keyboard for choosing language
async def settings_inline_keyboard(state):
    cur_language = await get_bot_language(state)
    channels_kb_list = [
        [InlineKeyboardButton(text=language[0] if language[1] != cur_language else language[0] + await localise("Current option", state), callback_data=language[1])] for language in digest_languages
    ]
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)


def digest_bot_addition_languages_keyboard():
    channels_kb_list = [
        [InlineKeyboardButton(text=language, callback_data=language)] for language in digest_languages
    ]
    channels_kb_list.append([InlineKeyboardButton(text="❌Without language", callback_data="without_language")])
    channels_kb_list.append([return_back_inline_button])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)
