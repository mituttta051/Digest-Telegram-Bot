# Import built-in packages
import unittest

# Import project files
from content.FSMs.settings_FSMs import SettingsFSM
from content.handlers.settings_handlers import bot_settings


class TestBotSettings(unittest.TestCase):
    async def test_sets_state_to_settings(self):
        from aiogram.fsm.context import FSMContext
        from aiogram.types import Message
        from unittest.mock import AsyncMock

        state = AsyncMock(FSMContext)
        message = AsyncMock(Message)
        message.text = "⚙️Settings"

        await bot_settings(message, state)

        state.set_state.assert_called_once_with(SettingsFSM.settings)

    async def test_sends_welcome_message(self):
        from aiogram.fsm.context import FSMContext
        from aiogram.types import Message
        from unittest.mock import AsyncMock, patch

        state = AsyncMock(FSMContext)
        message = AsyncMock(Message)
        message.text = "⚙️Settings"

        with patch('content.keyboards.settings_keyboards.settings_reply_keyboard', new_callable=AsyncMock) as mock_keyboard:
            with patch('content.handlers.settings_handlers.localise', new_callable=AsyncMock) as mock_localise:
                mock_localise.return_value = "Welcome to the settings!"
                await bot_settings(message, state)

                message.answer.assert_called_once_with("Welcome to the settings!", reply_markup=mock_keyboard.return_value)

    async def test_message_object_is_none(self):
        from aiogram.fsm.context import FSMContext
        from unittest.mock import AsyncMock
        import pytest

        state = AsyncMock(FSMContext)
        message = None

        with pytest.raises(AttributeError):
            await bot_settings(message, state)

    async def test_message_text_is_none(self):
        from aiogram.fsm.context import FSMContext
        from aiogram.types import Message
        from unittest.mock import AsyncMock
        import pytest

        state = AsyncMock(FSMContext)
        message = AsyncMock(Message)
        message.text = None

        with pytest.raises(AttributeError):
            await bot_settings(message, state)
