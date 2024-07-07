from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery


from content.handlers.digest_handlers import digest_edit

# Dependencies:
# pip install pytest-mock
import pytest

class TestDigestEdit:

    #  Acknowledges the edit selection with a callback answer
    @pytest.mark.asyncio
    async def test_acknowledges_edit_selection(self, mocker):
        # Arrange
        callback_query = mocker.Mock(spec=CallbackQuery)
        state = mocker.Mock(spec=FSMContext)
        callback_query.data = "digest_edit"
        callback_query.message.html_text = "Initial digest text"
    
        # Act
        await digest_edit(callback_query, state)
    
        # Assert
        callback_query.answer.assert_called_once_with('You chose "Edit"')

    #  Callback query data is missing or malformed
    @pytest.mark.asyncio
    async def test_callback_query_data_missing_or_malformed(self, mocker):
        # Arrange
        callback_query = mocker.Mock(spec=CallbackQuery)
        state = mocker.Mock(spec=FSMContext)
        callback_query.data = None  # Simulate missing data
    
        # Act and Assert
        with pytest.raises(AttributeError):
            await digest_edit(callback_query, state)
