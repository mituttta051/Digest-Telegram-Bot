import asyncio
from create_bot import bot, dp
from handlers.start import start_router
from handlers.generate import generate_router
from handlers.channel_messages import channel_messages_router


async def main():
    dp.include_router(start_router)
    dp.include_router(generate_router)
    dp.include_router(channel_messages_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
