# A file that will contain general message, command and callback handlers from settings branch

# Import downloaded packages
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

# Import project files
from content.FSMs.settings_FSMs import SettingsFSM
from content.handlers.general_handlers import bot_start
import content.keyboards.settings_keyboards as sk
import content.keyboards.general_keyboards as gk
from create_bot import cur, conn
from resources.locales.buttons import buttons
from resources.locales.translation_dictionary import localise
from utils.botUtils import get_channels_with_permissions, get_bot_language

# Create a router instance for settings-related message and callback handlers
settings_router = Router()


# Define a handler for the "Settings" command
@settings_router.message(F.text.in_(buttons["settings"]))
async def bot_settings(message: Message, state: FSMContext):
    """
    Asynchronous function to handle the "Settings" command.

    This function is triggered when a user sends a message with the text "Settings". It sends a welcome message to the
    settings menu and provides an inline keyboard for navigating the settings.

    Args:
        message (Message): The incoming message object containing the "Settings" text.
        :param message:
        :param state:
    """

    await state.set_state(SettingsFSM.settings)

    await message.answer(await localise("Welcome to the settings!", state),
                         reply_markup=await sk.settings_reply_keyboard(state))


@settings_router.message(F.text.in_(buttons["back_button"]), SettingsFSM.settings)
async def settings_back(message: Message, state: FSMContext):
    """
    Asynchronous function to handle the "Return back" callback query from the settings.

    This function is triggered when a user selects the "Return back" option via a callback query while in the settings.
    It acknowledges the selection and returns the user to the main menu by calling the `bot_start` function.

    Args:
        callback (CallbackQuery): The callback query object with the "settings_back" data.
        :param message:
        :param state:
    """

    # await state.clear()

    # Return to the main menu
    await bot_start(message, state)


@settings_router.message(F.text.in_(buttons["bot_language"]), SettingsFSM.settings)
async def choose_bot_language(message: Message, state: FSMContext):
    await state.set_state(SettingsFSM.change_language)

    await message.answer(await localise("Choose language", state),
                         reply_markup=await sk.settings_inline_keyboard(state))


@settings_router.callback_query(F.data == "back", SettingsFSM.change_language)
async def settings_back_to_settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.settings)

    await callback.answer(await localise("You return back", state))

    await bot_settings(callback.message, state)


@settings_router.callback_query(SettingsFSM.change_language)
async def chose_bot_language(callback: CallbackQuery, state: FSMContext):
    selected_language = callback.data

    last = await get_bot_language(state)

    await state.set_state(SettingsFSM.selected_bot_language)

    await state.update_data(selected_bot_language=selected_language)

    await state.set_state(SettingsFSM.settings)

    if last != selected_language:
        await callback.message.edit_text(await localise("Choose language", state),
                                         reply_markup=await sk.settings_inline_keyboard(state))

    await callback.answer(await localise("You chose ", state) + callback.data)

    await bot_settings(callback.message, state)


@settings_router.message(F.text.in_(buttons["channel_settings"]), SettingsFSM.settings)
async def choose_channel(message: Message, state: FSMContext):
    await state.set_state(SettingsFSM.choose_channel)

    channels = await get_channels_with_permissions(message.chat.id)

    await message.answer(await localise("Choose a channel", state),
                         reply_markup=await gk.channels_keyboard(channels, state))


@settings_router.callback_query(F.data == "back", SettingsFSM.choose_channel)
async def choose_channel_back_to_settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.settings)

    await callback.answer(await localise("You return back", state))

    await bot_settings(callback.message, state)


@settings_router.callback_query(SettingsFSM.choose_channel)
async def channel_settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.channel_settings)
    await state.update_data(channel_id=callback.data)

    await callback.answer(await localise("You chose channel", state))  # todo: channel name

    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.callback_query(F.data == "back", SettingsFSM.channel_settings)
async def channel_settings_back_to_settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.settings)

    await callback.answer(await localise("You return back", state))

    await bot_settings(callback.message, state)


@settings_router.callback_query(F.data == "main_language", SettingsFSM.channel_settings)
async def choose_main_language(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channel = data.get('channel_id')
    await state.set_state(SettingsFSM.main_language)
    cur.execute("SELECT main_language FROM channels WHERE channel_id = ?", (channel,))
    language = cur.fetchone()
    languages = {"en": "English", "ru": "Russia"}
    # str(languages[language[0]])

    await callback.answer(await localise("Choose one of the options", state))

    await callback.message.answer(await localise("Choose the main language for digest", state),
                                  reply_markup=await sk.digest_bot_languages_keyboard(state))

@settings_router.callback_query(F.data == "addition_language", SettingsFSM.channel_settings)
async def choose_addition_language(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channel = data.get('channel_id')
    await state.set_state(SettingsFSM.addition_language)
    cur.execute("SELECT additional_language FROM channels WHERE channel_id = ?", (channel,))
    language = cur.fetchone()
    languages = {"en": "English", "ru": "Russia", "no": "not selected"}
    await callback.answer(await localise("Choose one of the options", state))
    await callback.message.answer(await localise("Choose the addition language for digest", state),
                                  reply_markup=await sk.digest_bot_addition_languages_keyboard(state))


@settings_router.callback_query(F.data == "back", SettingsFSM.main_language or SettingsFSM.addition_language)
async def choose_main_language_back_to_channel_settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.channel_settings)

    await callback.answer(await localise("You return back", state))

    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.callback_query(SettingsFSM.main_language)
async def chose_main_language(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.channel_settings)
    data = await state.get_data()
    channel_id = data.get('channel_id')
    await callback.answer(await localise("You chose ", state) + callback.data)
    new_language = "?"
    if callback.data == "🇬🇧English":
        new_language = "en"
    elif callback.data == "🇷🇺Russian":
        new_language = "ru"

    if new_language != "?":
        cur.execute("UPDATE channels SET main_language = ? WHERE channel_id = ?", (new_language, channel_id))
    conn.commit()
    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.callback_query(SettingsFSM.addition_language)
async def chose_addition_language(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.channel_settings)
    data = await state.get_data()
    channel_id = data.get('channel_id')
    await callback.answer(await localise("You chose ", state) + callback.data)
    new_language = "?"
    if callback.data == "🇬🇧English":
        new_language = "en"
    elif callback.data == "without_language":
        new_language = "no"
    elif callback.data == "🇷🇺Russian":
        new_language = "ru"

    if new_language != "?":
        cur.execute("UPDATE channels SET additional_language = ? WHERE channel_id = ?", (new_language, channel_id))
    conn.commit()
    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))
