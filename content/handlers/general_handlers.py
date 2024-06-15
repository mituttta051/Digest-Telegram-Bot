# A file that will contain general message, command and callback handlers
# Import downloaded packages
from aiogram import Router, F
from aiogram.filters import CommandStart, ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR
from aiogram.types import Message, ChatMemberUpdated

# Import project files
import content.keyboards.general_keyboards as gk

general_router = Router()


# /start a.k.a. main menu command
@general_router.message(CommandStart())
async def bot_start(message: Message):
    await message.answer("Hello!", reply_markup=gk.start_reply_keyboard)


# Help command
@general_router.message(F.text == "Help")
async def bot_help(message: Message):
    await message.answer("I'm going to help you!")


@general_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR))
async def bot_added_as_admin(event: ChatMemberUpdated):
    print(event.chat.id, event.chat.title, "Added")


@general_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=ADMINISTRATOR >> IS_NOT_MEMBER))
async def bot_removed_from_channel(event: ChatMemberUpdated):
    print(event.chat.id, event.chat.title, "Removed")


@general_router.channel_post()
async def get_channel_post(message: Message):
    print(message.text, message.chat.id)
