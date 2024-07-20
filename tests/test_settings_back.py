# Import built-in packages
import unittest

# Import downloaded packages
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

# Import project files
from content.handlers.settings_handlers import settings_back


class TestSettingsBack(unittest.TestCase):

    async def test_clears_fsm_state_on_back_message(self):
        mock_message = unittest.mock.Mock(spec=Message)
        mock_state = unittest.mock.Mock(spec=FSMContext)
        mock_state.clear = unittest.mock.AsyncMock()
        mock_bot_start = unittest.mock.patch('content.handlers.settings_handlers.bot_start', new_callable=unittest.mock.AsyncMock)
        await settings_back(mock_message, mock_state)
        mock_state.clear.assert_called_once()
        mock_bot_start.assert_awaited_once_with(mock_message)

    async def test_calls_bot_start_after_clearing_state(self):
        mock_message = unittest.mock.Mock(spec=Message)
        mock_state = unittest.mock.Mock(spec=FSMContext)
        mock_state.clear = unittest.mock.AsyncMock()
        mock_bot_start = unittest.mock.patch('content.handlers.settings_handlers.bot_start', new_callable=unittest.mock.AsyncMock)
        await settings_back(mock_message, mock_state)
        mock_bot_start.assert_awaited_once_with(mock_message)

    async def test_handles_already_cleared_state(self):
        mock_message = unittest.mock.Mock(spec=Message)
        mock_state = unittest.mock.Mock(spec=FSMContext)
        mock_state.clear = unittest.mock.AsyncMock(side_effect=Exception("State already cleared"))
        mock_bot_start = unittest.mock.patch('content.handlers.settings_handlers.bot_start', new_callable=unittest.mock.AsyncMock)
        with self.assertRaises(Exception):
            await settings_back(mock_message, mock_state)
        mock_bot_start.assert_not_awaited()

    async def test_processes_back_message_not_in_settings_state(self):
        mock_message = unittest.mock.Mock(spec=Message)
        mock_state = unittest.mock.Mock(spec=FSMContext)
        mock_state.clear = unittest.mock.AsyncMock()
        mock_bot_start = unittest.mock.patch('content.handlers.settings_handlers.bot_start', new_callable=unittest.mock.AsyncMock)
        await settings_back(mock_message, mock_state)
        mock_bot_start.assert_awaited_once_with(mock_message)

    async def test_handles_missing_or_corrupted_state_data(self):
        mock_message = unittest.mock.Mock(spec=Message)
        mock_state = unittest.mock.Mock(spec=FSMContext)
        mock_state.clear = unittest.mock.AsyncMock(side_effect=Exception("Corrupted state data"))
        mock_bot_start = unittest.mock.patch('content.handlers.settings_handlers.bot_start', new_callable=unittest.mock.AsyncMock)
        with self.assertRaises(Exception):
            await settings_back(mock_message, mock_state)
        mock_bot_start.assert_not_awaited()
