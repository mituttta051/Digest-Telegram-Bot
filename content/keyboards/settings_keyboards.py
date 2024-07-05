# A file that will store settings branch keyboards

# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from resources.locales.translation_dictionary import localise


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


# Create an inline keyboard for choosing language
async def settings_inline_keyboard(state):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await localise("🇷🇺Russian", state), callback_data="ru")],
        [InlineKeyboardButton(text=await localise("🇬🇧English", state), callback_data="en")],
        [InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")]
    ])


async def channel_settings_inline_keyboard(state):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await localise("🛠API", state), callback_data="api")],
        [InlineKeyboardButton(text=await localise("🌍Main language", state), callback_data="main_language")],
        [InlineKeyboardButton(text=await localise("🌎Addition language", state),
                              callback_data="addition_language")],
        [InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")]
    ])


digest_languages = ["🇷🇺Russian", "🇬🇧English"]


async def digest_bot_languages_keyboard(state):
    channels_kb_list = [
        [InlineKeyboardButton(text=language, callback_data=language)] for language in digest_languages
    ]
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)
