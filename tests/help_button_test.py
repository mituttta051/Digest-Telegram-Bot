import pytest
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Chat, User
from aiogram.dispatcher.router import Router
from unittest.mock import AsyncMock
from content.handlers.general_handlers import bot_help, gk
from config import BOT_TOKEN
from datetime import datetime

@pytest.fixture
def bot():
    return Bot(token=BOT_TOKEN)

@pytest.fixture
def dispatcher():
    return Dispatcher()

@pytest.fixture
def router():
    return Router()

@pytest.fixture
def message():
    msg = Message(
        message_id=1,
        date=datetime.utcnow(),  # Provide a valid datetime
        chat=Chat(id=1, type="private"),
        from_user=User(id=1, is_bot=False, first_name="Test"),
        text="❓Help"
    )
    msg.answer = AsyncMock()
    return msg

@pytest.mark.asyncio
async def test_bot_help(bot, dispatcher, router, message):
    # Register the handler
    router.message.register(bot_help, equals="❓Help")
    dispatcher.include_router(router)

    # Process the message
    await dispatcher.process_update(bot, message)

    # Assert that the message was answered with the correct text and reply_markup
    message.answer.assert_called_once_with(
        """<b>Here's how you can use our Digest Bot:</b>

    ⚙️ <b>Settings</b>
      -  Change bot language: Select the bot interface language for ease of use.
      -  Change LLM API key: List of language models that the bot can use for generating responses.

    📝 <b>Create Digest</b>
      -  The bot will automatically create and send a summary of posts for the selected period. You can change or confirm the generated text before publishing.""",
        reply_markup=gk.start_reply_keyboard,
        parse_mode="HTML"
    )