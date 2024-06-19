# A file that will store digest branch keyboards

# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Buttons to choose digest period
week_period_inline_button = InlineKeyboardButton(text="Week (7 days)", callback_data="7")

# Buttons connected with digest activity
approve_inline_button = InlineKeyboardButton(text="Approve", callback_data="digest_approve")
edit_inline_button = InlineKeyboardButton(text="Edit", callback_data="digest_edit")
cancel_inline_button = InlineKeyboardButton(text="Cancel", callback_data="digest_cancel")
regenerate_inline_button = InlineKeyboardButton(text="Regenerate", callback_data="digest_regenerate")
cancel_editing_inline_button = InlineKeyboardButton(text="Cancel editing", callback_data="cancel_editing")

# Create an inline keyboard for digest actions
digest_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [approve_inline_button],
    [edit_inline_button],
    [cancel_inline_button],
    [regenerate_inline_button]
])

# Create an inline keyboard for supported period selection
supported_period_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [week_period_inline_button]
])


# Define a function to create an inline keyboard for channel selection
def channels_keyboard(channels: list[(str, str)]) -> InlineKeyboardMarkup:
    """
    Function to generate an inline keyboard for selecting channels.

    This function takes a list of tuples where each tuple contains a channel ID and a channel name. It creates an
    inline keyboard with buttons for each channel, where the button text is the channel name and the callback data is
    the channel ID.

    Args:
        channels (list of tuples): A list of tuples where each tuple contains a channel ID and a channel name.

    Returns:
        InlineKeyboardMarkup: An inline keyboard with buttons for each channel.
    """
    channels_kb_list = [
        [InlineKeyboardButton(text=name, callback_data=str(channel_id))] for (channel_id, name) in channels
    ]
    return InlineKeyboardMarkup(inline_keyboard=channels_kb_list)
