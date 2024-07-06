

from content.handlers.general_handlers import get_post

import pytest

class TestGetPost:

    #  correctly stores a message in the database
    @pytest.mark.asyncio
    async def test_correctly_stores_message_in_database(self, mocker):
        from aiogram.types import Message, Chat
        from datetime import datetime
        import sqlite3

        # Mocking the database connection and cursor
        mock_conn = mocker.patch('utils.databaseUtils.conn', autospec=True)
        mock_cur = mock_conn.cursor.return_value

        # Mocking the message object
        mock_message = mocker.Mock(spec=Message)
        mock_message.chat.id = -1001234567890
        mock_message.message_id = 123
        mock_message.html_text = "<b>Test Message</b>"

        # Mocking the datetime
        mock_datetime = mocker.patch('utils.databaseUtils.datetime')
        mock_datetime.now.return_value = datetime(2023, 1, 1)

        # Importing the function to test
        from content.handlers.general_handlers import get_post

        # Running the function
        await get_post(mock_message, mocker.Mock())

        # Asserting the database insert was called with correct parameters
        table_name = "messages_1001234567890"
        message_url = "https://t.me/c/234567890/123"
        mock_cur.execute.assert_called_once_with(
            f"""INSERT INTO {table_name} (date, text, link) VALUES (?, ?, ?)""",
            (datetime(2023, 1, 1), "<b>Test Message</b>", message_url)
        )
        mock_conn.commit.assert_called_once()

    #  handles a message with special characters in the text
    @pytest.mark.asyncio
    async def test_handles_message_with_special_characters(self, mocker):
        from aiogram.types import Message, Chat
        from datetime import datetime
        import sqlite3

        # Mocking the database connection and cursor
        mock_conn = mocker.patch('utils.databaseUtils.conn', autospec=True)
        mock_cur = mock_conn.cursor.return_value

        # Mocking the message object with special characters
        mock_message = mocker.Mock(spec=Message)
        mock_message.chat.id = -1001234567890
        mock_message.message_id = 124
        mock_message.html_text = "<b>Test & Message @ with # special $ characters!</b>"

        # Mocking the datetime
        mock_datetime = mocker.patch('utils.databaseUtils.datetime')
        mock_datetime.now.return_value = datetime(2023, 1, 1)

        # Importing the function to test
        from content.handlers.general_handlers import get_post

        # Running the function
        await get_post(mock_message, mocker.Mock())

        # Asserting the database insert was called with correct parameters
        table_name = "messages_1001234567890"
        message_url = "https://t.me/c/234567890/124"
        mock_cur.execute.assert_called_once_with(
            f"""INSERT INTO {table_name} (date, text, link) VALUES (?, ?, ?)""",
            (datetime(2023, 1, 1), "<b>Test & Message @ with # special $ characters!</b>", message_url)
        )
        mock_conn.commit.assert_called_once()
