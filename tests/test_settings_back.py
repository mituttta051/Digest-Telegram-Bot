from aiogram.fsm.context import FSMContext


from content.handlers.settings_handlers import settings_back
from aiogram.types import Message

# Dependencies:
# pip install pytest-mock
import pytest

class TestSettingsBack:

    #  Clears the FSM state when "⬅️Back" message is received
    @pytest.mark.asyncio
    async def test_clears_fsm_state_on_back_message(self, mocker):
        # Arrange
        mock_message = mocker.Mock(spec=Message)
        mock_state = mocker.Mock(spec=FSMContext)
        mock_bot_start = mocker.patch('content.handlers.settings_handlers.bot_start', new_callable=mocker.AsyncMock)
    
        # Act
        await settings_back(mock_message, mock_state)
    
        # Assert
        mock_state.clear.assert_called_once()
        mock_bot_start.assert_awaited_once_with(mock_message)

    #  Handles the "⬅️Back" message when FSM state is already cleared
    @pytest.mark.asyncio
    async def test_handles_back_message_when_state_cleared(self, mocker):
        # Arrange
        mock_message = mocker.Mock(spec=Message)
        mock_state = mocker.Mock(spec=FSMContext)
        mock_state.clear = mocker.AsyncMock()
        mock_bot_start = mocker.patch('content.handlers.settings_handlers.bot_start', new_callable=mocker.AsyncMock)
    
        # Act
        await settings_back(mock_message, mock_state)
    
        # Assert
        mock_state.clear.assert_called_once()
        mock_bot_start.assert_awaited_once_with(mock_message)
