from aiogram.fsm.state import StatesGroup, State


class SettingsFSM(StatesGroup):
    settings = State()
    change_language = State()
    choose_channel = State()
    channel_settings = State()
    main_language = State()
    addition_language = State()
    llms = State()
    llm_ygpt = State()
    ygpt_api = State()
    ygpt_id = State()
    data = State()
