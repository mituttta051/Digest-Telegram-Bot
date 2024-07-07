from aiogram.fsm.state import StatesGroup, State


class SettingsFSM(StatesGroup):
    settings = State()
    change_language = State()
    choose_channel = State()
    channel_settings = State()
    main_language = State()
    addition_language = State()
    selected_bot_language = State()
