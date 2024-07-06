

from content.handlers.settings_handlers import bot_settings, SettingsFSM

import pytest

class TestBotSettings:

    #  Function sets the state to SettingsFSM.settings
    @pytest.mark.asyncio
    async def test_sets_state_to_settings(self):
        from aiogram.fsm.context import FSMContext
        from aiogram.types import Message
        from unittest.mock import AsyncMock

        state = AsyncMock(FSMContext)
        message = AsyncMock(Message)
        message.text = "⚙️Settings"

        await bot_settings(message, state)

        state.set_state.assert_called_once_with(SettingsFSM.settings)

    #  Message object is None or invalid
    @pytest.mark.asyncio
    async def test_message_object_none_or_invalid(self):
        from aiogram.fsm.context import FSMContext
        from aiogram.types import Message
        from unittest.mock import AsyncMock

        state = AsyncMock(FSMContext)
        message = None

        with pytest.raises(AttributeError):
            await bot_settings(message, state)

        message = AsyncMock(Message)
        message.text = None

        with pytest.raises(AttributeError):
            await bot_settings(message, state)
