# Import built-in packages
from typing import Union

# Import downloaded packages
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Import project files
from resources.locales.translation_dictionary import localise
from utils.botUtils import get_bot_language
from utils.databaseUtils import get_additional_language, get_main_language, get_auto_digest_data, get_api_key, \
    get_folder_id


# Create a reply keyboard for settings actions
async def settings_reply_keyboard(state: FSMContext) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=await localise("🌍Bot language", state)),
         KeyboardButton(text=await localise("⚙️Channel settings", state))],
        [KeyboardButton(text=await localise("⬅️Back", state))]
    ],
        resize_keyboard=True,
        input_field_placeholder=await localise("Select a menu button", state),
        one_time_keyboard=True
    )


async def channel_settings_inline_keyboard(state: FSMContext) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await localise("🛠API", state), callback_data="api")],
        [InlineKeyboardButton(text=await localise("🌍Main language", state), callback_data="main_language")],
        [InlineKeyboardButton(text=await localise("🌎Additional language", state),
                              callback_data="additional_language")],
        [InlineKeyboardButton(text=await localise("🤖Auto digest", state), callback_data="auto_digest")],
        [InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")]
    ])


async def auto_digest_settings_keyboard(channel_id: Union[str, int], state: FSMContext) -> InlineKeyboardMarkup:
    data = get_auto_digest_data(channel_id)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await localise("🕒Auto digest time", state), callback_data="auto_digest_time")],
        [InlineKeyboardButton(text=await localise(
            "🟩Turn on auto digest" if data.get("auto_digest", "no") == "no" else "🟥Turn off auto digest", state),
                              callback_data="auto_digest_switch")],
        [InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")]
    ])


async def settings_back_button_keyboard(state: FSMContext) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")]
    ])


digest_languages = [("🇷🇺Russian", "ru"), ("🇬🇧English", "en")]  # Todo: Refactor to dict. Remove emoji from languages
llms = [("YGPT", "ygpt"), ("Default(free) model", "free_model")]  # Todo: Refactor to dict


async def digest_bot_languages_keyboard(channel_id: Union[str, int], state: FSMContext) -> InlineKeyboardMarkup:
    main_language = get_main_language(channel_id)
    channels_kb_list = [
        [InlineKeyboardButton(
            # Todo: Rework hardcoded if-statement
            text=language[0] if language[1] != main_language else language[0] + await localise("Current option", state),
            callback_data=language[1])] for language in digest_languages
    ]
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)


async def digest_bot_llm_keyboard(channel_id: Union[str, int], state: FSMContext) -> InlineKeyboardMarkup:
    api = get_api_key(channel_id)
    id = get_folder_id(channel_id)  # Todo: Rename element
    channels_kb_list = [
        [InlineKeyboardButton(
            # Todo: Rework hardcoded if-statement
            text=llm[0] if (llm[0] == 'YGPT' and api == id) or (llm[0] != 'YGPT' and api != id) else llm[
                                                                                                         0] + await localise(
                "Current option", state),
            callback_data=llm[1])] for llm in llms
    ]
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)


# Create an inline keyboard for choosing language
async def settings_inline_keyboard(state: FSMContext) -> InlineKeyboardMarkup:
    cur_language = await get_bot_language(state)
    channels_kb_list = [
        [InlineKeyboardButton(
            # Todo: Rework hardcoded if-statement
            text=language[0] if language[1] != cur_language else language[0] + await localise("Current option", state),
            callback_data=language[1])] for language in digest_languages
    ]
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)


async def digest_bot_additional_languages_keyboard(channel_id: Union[str, int],
                                                   state: FSMContext) -> InlineKeyboardMarkup:
    additional_language = get_additional_language(channel_id)
    channels_kb_list = [
        [InlineKeyboardButton(
            # Todo: Rework hardcoded if-statement
            text=language[0] if language[1] != additional_language else language[0] + await localise("Current option",
                                                                                                     state),
            callback_data=language[1])] for language in digest_languages
    ]
    if additional_language == "no":
        channels_kb_list.append(
            [InlineKeyboardButton(
                text=await localise("❌Without language", state) + await localise("Current option", state),
                callback_data="without_language")])
    else:
        channels_kb_list.append(
            [InlineKeyboardButton(text=await localise("❌Without language", state), callback_data="without_language")])
    channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)
