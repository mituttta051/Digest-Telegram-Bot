# A file that will store digest branch keyboards

# Import downloaded packages
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from resources.locales.translation_dictionary import localise


# Create an inline keyboard for digest actions
async def digest_inline_keyboard(state):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await localise("✅Approve", state), callback_data="digest_approve")],
        [InlineKeyboardButton(text=await localise("✏️Edit", state), callback_data="digest_edit")],
        [InlineKeyboardButton(text=await localise("❌Cancel", state), callback_data="digest_cancel")],
        [InlineKeyboardButton(text=await localise("🔄Regenerate", state), callback_data="digest_regenerate")]
    ])


# Create an inline keyboard for supported period selection
async def supported_period_inline_keyboard(state):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await localise("Week (7 days)", state), callback_data="7")],
        [InlineKeyboardButton(text=await localise("2 weeks (14 days)", state), callback_data="14")],
        [InlineKeyboardButton(text=await localise("1 Month (30 days)", state), callback_data="30")],
        [InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")]
    ])


async def return_back_button_keyboard(state):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=await localise("⬅️Back", state), callback_data="back")]
    ])
