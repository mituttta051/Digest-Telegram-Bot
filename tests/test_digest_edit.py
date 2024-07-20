# Import built-in packages
import unittest

# Import project files
from content.handlers.digest_handlers import digest_edit


class TestDigestEdit(unittest.TestCase):
    async def test_acknowledges_edit_selection(self):
        from unittest.mock import AsyncMock, patch
        from aiogram.types import CallbackQuery
        from aiogram.fsm.context import FSMContext

        callback_query = AsyncMock(spec=CallbackQuery)
        state = AsyncMock(spec=FSMContext)
        callback_query.data = "digest_edit"
        callback_query.message.html_text = "Initial digest text"

        with patch('content.handlers.digest_handlers.localise', return_value="You chose \"Edit\""):
            await digest_edit(callback_query, state)

        callback_query.answer.assert_called_once_with("You chose \"Edit\"")

    async def test_stores_initial_text_in_state(self):
        from unittest.mock import AsyncMock, patch
        from aiogram.types import CallbackQuery
        from aiogram.fsm.context import FSMContext

        callback_query = AsyncMock(spec=CallbackQuery)
        state = AsyncMock(spec=FSMContext)
        callback_query.data = "digest_edit"
        callback_query.message.html_text = "Initial digest text"

        with patch('content.handlers.digest_handlers.localise', return_value="You chose \"Edit\""):
            await digest_edit(callback_query, state)

        state.update_data.assert_called_once_with(initial_text="Initial digest text")

    async def test_callback_query_data_missing_or_malformed(self):
        from unittest.mock import AsyncMock, patch
        from aiogram.types import CallbackQuery
        from aiogram.fsm.context import FSMContext

        callback_query = AsyncMock(spec=CallbackQuery)
        state = AsyncMock(spec=FSMContext)
        callback_query.data = None

        with self.assertRaises(AttributeError):
            await digest_edit(callback_query, state)

    async def test_state_context_not_initialized(self):
        from unittest.mock import AsyncMock, patch
        from aiogram.types import CallbackQuery
        from aiogram.fsm.context import FSMContext

        callback_query = AsyncMock(spec=CallbackQuery)
        state = None  # Simulate uninitialized state context

        with self.assertRaises(AttributeError):
            await digest_edit(callback_query, state)

    #  Callback message does not contain html_text
    async def test_callback_message_no_html_text(self):
        from unittest.mock import AsyncMock, patch
        from aiogram.types import CallbackQuery
        from aiogram.fsm.context import FSMContext

        callback_query = AsyncMock(spec=CallbackQuery)
        state = AsyncMock(spec=FSMContext)
        callback_query.data = "digest_edit"
        callback_query.message.html_text = None  # Simulate missing html_text

        with self.assertRaises(AttributeError):
            await digest_edit(callback_query, state)
