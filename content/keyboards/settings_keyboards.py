# A file that will store settings branch keyboards

# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from resources.locales.translation_dictionary import localise
from utils.botUtils import get_bot_language
from utils.databaseUtils import get_addition_language, get_main_language, get_api_key, get_folder_id

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
llms = [("YGPT", "ygpt"), ("Default(free) model", "free_model")]

async def digest_bot_languages_keyboard(channel_id, state):
    main_language = get_main_language(channel_id)
    channels_kb_list = [
        [InlineKeyboardButton(
            text=language[0] if language[1] != main_language else language[0] + await localise("Current option", state),
            callback_data=language[1])] for language in digest_languages
    ]
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)

async def digest_bot_llm_keyboard(channel_id, state):
    api = get_api_key(channel_id)
    id = get_folder_id(channel_id)
    channels_kb_list = [
        [InlineKeyboardButton(
            text=llm[0] if (llm[0] == 'YGPT' and api == id) or (llm[0] != 'YGPT' and api != id) else llm[0] + await localise("Current option", state),
            callback_data=llm[1])] for llm in llms
    ]
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)


# Create an inline keyboard for choosing language
async def settings_inline_keyboard(state):
    cur_language = await get_bot_language(state)
    channels_kb_list = [
        [InlineKeyboardButton(
            text=language[0] if language[1] != cur_language else language[0] + await localise("Current option", state),
            callback_data=language[1])] for language in digest_languages
    ]
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)


async def digest_bot_addition_languages_keyboard(channel_id, state):
    addition_language = get_addition_language(channel_id)
    channels_kb_list = [
        [InlineKeyboardButton(
            text=language[0] if language[1] != addition_language else language[0] + await localise("Current option",
                                                                                                   state),
            callback_data=language[1])] for language in digest_languages
    ]
    if addition_language == "no":
        channels_kb_list.append(
            [InlineKeyboardButton(
                text=await localise("❌Without language", state) + await localise("Current option", state),
                callback_data="without_language")])
    else:
        channels_kb_list.append(
            [InlineKeyboardButton(text=await localise("❌Without language", state), callback_data="without_language")])
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)


