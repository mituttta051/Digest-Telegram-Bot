# A file that will contain general message, command and callback handlers from settings branch

# Import downloaded packages
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

# Import project files
from content.handlers.general_handlers import bot_start
import content.keyboards.settings_keyboards as sk

# Create a router instance for settings-related message and callback handlers
settings_router = Router()


# Define a handler for the "Settings" command
@settings_router.message(F.text == "Settings")
async def bot_settings(message: Message):
    """
    Asynchronous function to handle the "Settings" command.

    This function is triggered when a user sends a message with the text "Settings". It sends a welcome message to the
    settings menu and provides an inline keyboard for navigating the settings.

    Args:
        message (Message): The incoming message object containing the "Settings" text.
    """
    await message.answer("Welcome to the settings!", reply_markup=sk.settings_inline_keyboard)


# Define a handler for callback queries with data "settings_back"
@settings_router.callback_query(lambda callback: callback.data == "settings_back")
async def settings_back(callback: CallbackQuery):
    """
    Asynchronous function to handle the "Return back" callback query from the settings.

    This function is triggered when a user selects the "Return back" option via a callback query while in the settings.
    It acknowledges the selection and returns the user to the main menu by calling the `bot_start` function.

    Args:
        callback (CallbackQuery): The callback query object with the "settings_back" data.
    """
    # Acknowledge the "Return back" selection
    await callback.answer('You chose "Return back"')

    # Return to the main menu
    await bot_start(callback.message)
