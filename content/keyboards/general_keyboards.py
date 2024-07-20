# Import built-in packages
from typing import Union

# Import downloaded packages
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Import project files
from resources.locales.translation_dictionary import localise

return_back_button = InlineKeyboardButton(text="⬅️Back", callback_data="back")


# Define the start menu reply keyboard
async def start_reply_keyboard(state: FSMContext) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=await localise("✍🏼Create digest", state))],
        [KeyboardButton(text=await localise("❓Help", state)), KeyboardButton(text=await localise("⚙️Settings", state))]
    ],
        resize_keyboard=True,
        input_field_placeholder="Select a menu button",
        one_time_keyboard=True
    )


# Define a function to create an inline keyboard with multiple buttons
def make_inline_keyboard(*buttons: InlineKeyboardButton) -> InlineKeyboardMarkup:
    """
    Function to generate an inline keyboard with multiple buttons.

    This function takes a variable number of InlineKeyboardButton instances and arranges them into an inline keyboard.
    Each button is placed in its own row.

    Args:
        *buttons (InlineKeyboardButton): A variable number of InlineKeyboardButton instances.

    Returns:
        InlineKeyboardMarkup: An inline keyboard with the provided buttons.
    """
    inline_keyboard = []
    for button in buttons:
        inline_keyboard.append([button])

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# Define a function to create a keyboard with a single button of either reply or inline type
def one_button_keyboard(button_type: str, text: str) -> Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]:
    """
    Function to generate a keyboard with a single button of either reply or inline type.

    This function takes a button type ('reply' or 'inline') and a text for the button. It creates a keyboard with a
    single button of the specified type. If the button type is 'reply', a ReplyKeyboardMarkup is returned. If the
    button type is 'inline', an InlineKeyboardMarkup is returned.

    Args:
        button_type (str): The type of the button ('reply' or 'inline').
        text (str): The text to display on the button.

    Returns:
        Union[ReplyKeyboardMarkup, InlineKeyboardMarkup]: A keyboard with a single button of the specified type.
    """
    if button_type.lower() == "reply":
        return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=text)]], resize_keyboard=True, one_time_keyboard=True)
    elif button_type.lower() == "inline":
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, callback_data="empty-data")]])


# Define a function to create an inline keyboard for channel selection
async def channels_keyboard(channels: list[(str, str)], state: FSMContext) -> InlineKeyboardMarkup:
    """
    Function to generate an inline keyboard for selecting channels.

    This function takes a list of tuples where each tuple contains a channel ID and a channel name. It creates an
    inline keyboard with buttons for each channel, where the button text is the channel name and the callback data is
    the channel ID.

    Args:
        channels (list of tuples): A list of tuples where each tuple contains a channel ID and a channel name.
        state (aiogram.fsm.context.FSMContext): The state context object used to manage the finite state machine.

    Returns:
        InlineKeyboardMarkup (aiogram.types.inline_keyboard_markup): An inline keyboard with buttons for each channel.
    """
    channels_kb_list = [
        [InlineKeyboardButton(text=name, callback_data=str(channel_id))] for
        (channel_id, name, main_l, additional_l, auto_digest, auto_digest_date, api_key, folder_id) in channels
    ]
    if len(channels_kb_list) == 0:
        channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Add the bot to your channel first", state),
                                                      callback_data="back")])
    else:
        channels_kb_list.append([InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)
