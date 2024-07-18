# Import built-in packages
import unittest

# Import project files
from content.handlers.general_handlers import bot_help


class TestBotHelp(unittest.TestCase):
    async def test_responds_to_help_command_in_default_language(self):
        from aiogram.types import Message
        from aiogram.fsm.context import FSMContext
        from unittest.mock import AsyncMock, patch

        message = AsyncMock(spec=Message)
        state = AsyncMock(spec=FSMContext)
        message.text = "❓Help"
        message.answer = AsyncMock()

        with patch('content.keyboards.general_keyboards.start_reply_keyboard', AsyncMock()) as mock_keyboard:
            with patch('resources.locales.translation_dictionary.localise', AsyncMock(return_value="Settings")) as mock_localise:
                await bot_help(message, state)
                message.answer.assert_called_once_with("Settings", reply_markup=mock_keyboard.return_value)

    async def test_handles_missing_or_invalid_fsmcontext_gracefully(self):
        from aiogram.types import Message
        from unittest.mock import AsyncMock, patch

        message = AsyncMock(spec=Message)
        message.text = "❓Help"
        message.answer = AsyncMock()

        with patch('content.keyboards.general_keyboards.start_reply_keyboard', AsyncMock()) as mock_keyboard:
            with patch('resources.locales.translation_dictionary.localise', AsyncMock(return_value="Settings")) as mock_localise:
                await bot_help(message, None)
                message.answer.assert_called_once_with("Settings", reply_markup=mock_keyboard.return_value)
