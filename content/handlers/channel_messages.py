from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, ADMINISTRATOR
from aiogram.types import Message, ChatMemberUpdated

from utils.databaseUtils import put_message, put_channel

channel_messages_router = Router()


@channel_messages_router.channel_post()
async def get_post(message: Message):
    put_message(message, message.chat.id)


@channel_messages_router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR
    )
)
async def bot_added_as_admin(event: ChatMemberUpdated):
    put_channel(event.chat.id, event.chat.title)
