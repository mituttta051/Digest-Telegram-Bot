# Import downloaded packages
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

# Import project files
from content.FSMs.settings_FSMs import SettingsFSM
from content.handlers.general_handlers import bot_start
import content.keyboards.settings_keyboards as sk
import content.keyboards.general_keyboards as gk
from resources.locales.buttons import buttons
from resources.locales.translation_dictionary import localise
from utils.botUtils import get_channels_with_permissions, get_bot_language, get_data
from utils.databaseUtils import get_additional_language, get_main_language, update_main_language, \
    update_additional_language, update_bot_language, change_auto_digest, change_auto_digest_date, update_api_key, \
    update_folder_id, update_system_prompt
from content.schedulers.auto_digest_scheduler import update_scheduler

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
        message (aiogram.types.message): The incoming message object containing the "Settings" text.
        state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.
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
        message (aiogram.types.message): The incoming message object containing user id.
        state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.
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

    await state.set_state(SettingsFSM.data)  # Todo: Remove due to irrelevancy

    await state.update_data(selected_bot_language=selected_language)

    data = await state.get_data()

    update_bot_language(data.get("user_id", None), selected_language)

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

    if len(channels) == 0:
        # if there are no channels, need to return automatically
        await back_to_settings_auto(message, state)
    else:
        # Send a message with a keyboard to choose a channel
        await message.answer(await localise("Choose a channel", state),
                             reply_markup=await gk.channels_keyboard(channels, state))


async def back_to_settings_auto(message: Message, state: FSMContext) -> None:
    await message.answer(await localise("Add the bot to your channel first", state))

    # Start the bot from the settings menu
    await bot_settings(message, state)


@settings_router.callback_query(F.data == "back", SettingsFSM.choose_channel)
async def choose_channel_back_to_settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.settings)

    await callback.answer(await localise("You return back", state))

    await bot_settings(callback.message, state)


@settings_router.callback_query(SettingsFSM.choose_channel)
async def channel_settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.data)  # Todo: Remove due to irrelevancy
    await state.update_data(channel_id=callback.data)
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

    await callback.answer(await localise("Choose one of the options", state))

    await callback.message.answer(await localise("Choose the main language for digest", state),
                                  reply_markup=await sk.digest_bot_languages_keyboard(channel, state))


@settings_router.callback_query(F.data == "additional_language", SettingsFSM.channel_settings)
async def choose_additional_language(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channel = data.get('channel_id')
    await state.set_state(SettingsFSM.additional_language)
    await callback.answer(await localise("Choose one of the options", state))
    await callback.message.answer(await localise("Choose the additional language for digest", state),
                                  reply_markup=await sk.digest_bot_additional_languages_keyboard(channel, state))


@settings_router.callback_query(F.data == "api", SettingsFSM.channel_settings)
async def choose_llm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channel = data.get('channel_id')
    await state.set_state(SettingsFSM.llms)
    await callback.answer(await localise("Choose one of the options", state))
    await callback.message.answer(await localise("Choose the llm for your chanel", state),
                                  reply_markup=await sk.digest_bot_llm_keyboard(channel, state))


@settings_router.callback_query(F.data == "back",
                                SettingsFSM.main_language or SettingsFSM.additional_language)
async def choose_main_language_back_to_channel_settings(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.channel_settings)

    await callback.answer(await localise("You return back", state))

    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.callback_query(F.data == "back", SettingsFSM.llms)
async def choose_api_back(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.channel_settings)

    await callback.answer(await localise("You return back", state))

    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.callback_query(SettingsFSM.main_language)
async def chose_main_language(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.channel_settings)
    data = await state.get_data()
    channel_id = data.get('channel_id')
    last = get_main_language(channel_id)

    await callback.answer(await localise("You chose ", state) + callback.data)

    new_language = "?"
    if callback.data == "en":
        new_language = "en"
    elif callback.data == "ru":
        new_language = "ru"

    if new_language != "?":
        update_main_language(channel_id, new_language)

    if last != new_language and new_language != "?":
        await callback.message.edit_text(await localise("Choose the main language for digest", state),
                                         reply_markup=await sk.digest_bot_languages_keyboard(channel_id, state))

    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.callback_query(SettingsFSM.additional_language)
async def chose_additional_language(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.channel_settings)
    data = await state.get_data()
    channel_id = data.get('channel_id')
    last = get_additional_language(channel_id)

    await callback.answer(await localise("You chose ", state) + callback.data)

    # Todo: Refactor code below
    new_language = "?"
    if callback.data == "en":
        new_language = "en"
    elif callback.data == "without_language":
        new_language = "no"
    elif callback.data == "ru":
        new_language = "ru"

    if new_language != "?":
        update_additional_language(channel_id, new_language)

    if last != new_language and new_language != "?":
        await callback.message.edit_text(await localise("Choose the additional language for digest", state),
                                         reply_markup=await sk.digest_bot_additional_languages_keyboard(channel_id,
                                                                                                        state))

    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.callback_query(F.data == "auto_digest", SettingsFSM.channel_settings)
async def auto_digest_settings(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    data = await get_data(state)  # Todo: Replace with a state.get_data()
    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.auto_digest_settings_keyboard(data.get("channel_id", "0"),
                                                                                      state))
    await state.set_state(SettingsFSM.auto_digest)


@settings_router.callback_query(F.data == "auto_digest_switch", SettingsFSM.auto_digest)
async def auto_digest_switch(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await change_auto_digest(state)
    data = await get_data(state)  # Todo: Replace with a state.get_data()
    update_scheduler()
    await callback.message.edit_text(await localise("Choose one of the options", state),
                                     reply_markup=await sk.auto_digest_settings_keyboard(data.get("channel_id", "0"),
                                                                                         state))


@settings_router.callback_query(F.data == "back", SettingsFSM.auto_digest)
async def auto_digest_switch(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.channel_settings)

    await callback.answer(await localise("You return back", state))

    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.callback_query(F.data == "auto_digest_time", SettingsFSM.auto_digest)
async def auto_digest_switch(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.set_state(SettingsFSM.auto_digest_date)

    await callback.message.answer(await localise("auto digest time", state),
                                  reply_markup=await sk.settings_back_button_keyboard(state))


@settings_router.callback_query(F.data == "back", SettingsFSM.auto_digest_date)
async def auto_digest_switch(callback: CallbackQuery, state: FSMContext):
    await callback.answer(await localise("You return back", state))
    data = await get_data(state)  # Todo: Replace with a state.get_data()
    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.auto_digest_settings_keyboard(data.get("channel_id", "0"),
                                                                                      state))
    await state.set_state(SettingsFSM.auto_digest)


@settings_router.message(SettingsFSM.auto_digest_date)
async def auto_digest_switch(message: Message, state: FSMContext):
    # Todo: Reformat code below. Maybe use regexp
    args = message.html_text.split(" ")
    if len(args) != 2:
        await message.answer(await localise("Incorrect format. Try again", state))
        return
    time = args[0].split(":")
    if len(time) != 2:
        await message.answer(await localise("Incorrect format. Try again", state))
        return
    try:
        hours = int(time[0])
        minutes = int(time[1])
        day = int(args[1])
    except ValueError:
        await message.answer(await localise("Write valid numbers. Try again", state))
        return
    if hours < 0 or minutes < 0 or day < 1 or hours > 23 or minutes > 59 or day > 7:
        await message.answer(await localise(
            "auto digest interval error",
            state))
        return
    data = await get_data(state)  # Todo: Replace with a state.get_data()
    change_auto_digest_date(data.get("channel_id", "0"), f"{minutes} {hours} * * {day}")
    update_scheduler()
    await message.answer(await localise("You successfully changed the auto digest time", state))
    await message.answer(await localise("Choose one of the options", state),
                         reply_markup=await sk.auto_digest_settings_keyboard(data.get("channel_id", "0"),
                                                                             state))
    await state.set_state(SettingsFSM.auto_digest)


@settings_router.callback_query(F.data == "ygpt", SettingsFSM.llms)
async def choose_llm(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.ygpt_api)
    await callback.answer()
    await callback.message.answer(await localise("Enter api key", state))


@settings_router.callback_query(F.data == "free_model", SettingsFSM.llms)
async def free_model_llm(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.answer()
    channel_id = data.get('channel_id')
    update_api_key(channel_id, None)
    update_folder_id(channel_id, None)
    await state.set_state(SettingsFSM.channel_settings)
    await callback.message.answer(await localise("Current LLM changed", state))
    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.message(SettingsFSM.ygpt_api)
async def input_first_text(message: Message, state: FSMContext):
    data = await state.get_data()
    channel_id = data.get('channel_id')
    update_api_key(channel_id, message.text)
    await state.set_state(SettingsFSM.ygpt_id)
    await message.answer(await localise("Enter folder id", state))


@settings_router.message(SettingsFSM.ygpt_id)
async def input_second_text(message: Message, state: FSMContext):
    data = await state.get_data()
    channel_id = data.get('channel_id')
    update_folder_id(channel_id, message.text)
    await message.answer(await localise("Current LLM changed", state))
    await state.set_state(SettingsFSM.channel_settings)
    await message.answer(await localise("Choose one of the options", state),
                         reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.callback_query(F.data == "custom_system_prompt", SettingsFSM.channel_settings)
async def custom_system_prompt_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.custom_system_prompt)
    await callback.answer()
    await callback.message.answer(await localise("Write your system prompt", state),
                                  reply_markup=await sk.channel_settings_system_prompt_inline_keyboard(state))


@settings_router.callback_query(F.data == "back", SettingsFSM.custom_system_prompt)
async def back_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SettingsFSM.channel_settings)

    await callback.answer(await localise("You return back", state))

    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.callback_query(F.data == "remove_system_prompt", SettingsFSM.custom_system_prompt)
async def system_prompt_remove_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    channel_id = data.get('channel_id')
    update_system_prompt(channel_id, "")

    await state.set_state(SettingsFSM.channel_settings)

    await callback.answer()
    await callback.message.answer(await localise("You successfully removed the system prompt", state))
    await callback.message.answer(await localise("Choose one of the options", state),
                                  reply_markup=await sk.channel_settings_inline_keyboard(state))


@settings_router.message(SettingsFSM.custom_system_prompt)
async def new_system_prompt_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    channel_id = data.get('channel_id')
    update_system_prompt(channel_id, message.html_text)

    await state.set_state(SettingsFSM.channel_settings)

    await message.answer(await localise("You successfully changed the system prompt", state))
    await message.answer(await localise("Choose one of the options", state),
                         reply_markup=await sk.channel_settings_inline_keyboard(state))
