# A file that will contain general message, command and callback handlers

# Import downloaded packages
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR
from aiogram.types import Message, ChatMemberUpdated

# Import project files
import content.keyboards.general_keyboards as gk
from utils.databaseUtils import put_message, put_channel

# Create a router instance for general message, command, and callback handlers
general_router = Router()


# Define a handler for the /start command, which is the main menu command
@general_router.message(CommandStart())
async def bot_start(message: Message):
    """
    Asynchronous function to handle the /start command, which is the main menu command.

    This function is triggered when a user sends the /start command. It sends a greeting message with a reply keyboard
    to the user.

    Args:
        message (Message): The incoming message object containing the /start command.
    """
    await message.answer("Hello!", reply_markup=gk.start_reply_keyboard)


# Define a handler for the "Help" command
@general_router.message(F.text == "Help")
async def bot_help(message: Message):
    """
    Asynchronous function to handle the "Help" command.

    This function is triggered when a user sends a message with the text "Help". It sends a help message to the user.

    Args:
        message (Message): The incoming message object containing the "Help" text.
    """
    await message.answer("I'm going to help you!")


# Define a handler for when the bot is added as an administrator in a chat
@general_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated):
    """
    Asynchronous function to handle the event when the bot is added as an administrator in a chat.

    This function is triggered when the bot's status changes from not a member to an administrator in a chat. It stores
    the chat ID and title in the database.

    Args:
        event (ChatMemberUpdated): The event object containing the chat member status update.
    """
    put_channel(event.chat.id, event.chat.title)


# Define a handler for when the bot is removed from being an administrator in a chat
@general_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> IS_NOT_MEMBER))
async def bot_removed_from_channel(event: ChatMemberUpdated):
    """
    Asynchronous function to handle the event when the bot is removed from being an administrator in a chat.

    This function is triggered when the bot's status changes from an administrator to not a member in a chat. It prints
    the chat ID and title to the console.

    Args:
        event (ChatMemberUpdated): The event object containing the chat member status update.
    """
    print(event.chat.id, event.chat.title, "Removed")


# Define a handler for channel posts
@general_router.channel_post()
async def get_post(message: Message, bot: Bot):
    """
    Asynchronous function to handle channel posts.

    This function is triggered when a post is made in a channel where the bot is a member. It stores the message and
    the channel ID in the database.

    Args:
        message (Message): The incoming channel post message object.
        bot (Bot): The bot instance to get the bot's user ID.
    """
    if message.from_user.id != bot.id:
        put_message(message, message.chat.id)
