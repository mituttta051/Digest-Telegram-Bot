# A file that will store the general keyboards
# Or keyboards that doesn't belong to branches
from typing import Union

# Import downloaded packages
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Define the start menu reply keyboard
start_reply_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="✍🏼Create digest")],
    [KeyboardButton(text="❓Help"), KeyboardButton(text="⚙️Settings")]
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
