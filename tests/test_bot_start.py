# Import built-in packages
import unittest
from unittest.mock import AsyncMock, patch

# Import downloaded packages
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

# Import project files
from content.FSMs.settings_FSMs import SettingsFSM
from content.handlers.general_handlers import bot_start


class TestBotStart(unittest.TestCase):
    @patch('content.handlers.general_handlers.put_user')
    @patch('content.handlers.general_handlers.localise', new_callable=AsyncMock)
    @patch('content.keyboards.general_keyboards.start_reply_keyboard', new_callable=AsyncMock)
    async def test_user_sends_start_in_another_state(self, mock_start_reply_keyboard, mock_localise, mock_put_user):
        message = AsyncMock(spec=Message)
        message.from_user.id = 12345
        state = AsyncMock(spec=FSMContext)
        state.get_state.return_value = SettingsFSM.change_language.state
        mock_localise.return_value = "Welcome"
        mock_start_reply_keyboard.return_value = "keyboard"

        await bot_start(message, state)

        state.set_state.assert_called_once_with(SettingsFSM.data)
        state.update_data.assert_called_once_with(user_id=12345)
        mock_put_user.assert_called_once_with(12345)
        mock_localise.assert_called_once_with("Welcome", state)
        message.answer.assert_called_once_with("Welcome", reply_markup="keyboard")
