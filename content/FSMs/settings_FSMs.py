# Import downloaded packages
from aiogram.fsm.state import StatesGroup, State


class SettingsFSM(StatesGroup):
    """
        A class representing the finite state machine for managing the settings functionality.

        This class defines the states that the finite state machine can be in, which are used to track the
        user's progress through the settings.

        States:
            settings (aiogram.fsm.state.State): The state where the user is prompted to select a specific setting.
            change_language (aiogram.fsm.state.State): The state where the user is prompted to select a bot language.
            choose_channel (aiogram.fsm.state.State): The state in which the user is prompted to select a channel
            channel_settings (aiogram.fsm.state.State): The state in which the user is prompted to change the bot settings relative to the selected channel
            main_language (aiogram.fsm.state.State): The state where the user is prompted to choose main digest language
            additional_language (aiogram.fsm.state.State): The state where the user is prompted to choose additional digest language
            auto_digest (aiogram.fsm.state.State): The state where the user is prompted to select setting for automated digest publication
            auto_digest_date (aiogram.fsm.state.State): The state where the user is prompted to select a date for automated digest publication
            llms (aiogram.fsm.state.State): The state where the user is prompted to select large language model to be used for digest creation
            llm_ygpt (aiogram.fsm.state.State):
            ygpt_api (aiogram.fsm.state.State): The state where the user is prompted to insert YaGPT API key
            ygpt_id (aiogram.fsm.state.State): The state where the user is prompted to insert YaGPT id
            data (aiogram.fsm.state.State):
    """
    settings = State()
    change_language = State()
    choose_channel = State()
    channel_settings = State()
    main_language = State()
    additional_language = State()
    auto_digest = State()
    auto_digest_date = State()
    llms = State()
    llm_ygpt = State()  # Todo: Use state or remove it
    ygpt_api = State()
    ygpt_id = State()
    data = State()  # Todo: Use state properly or remove it due to irrelevancy
