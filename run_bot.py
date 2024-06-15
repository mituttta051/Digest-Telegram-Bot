import asyncio
from create_bot import bot, dp
from content.handlers.general_handlers import general_router
from content.handlers.digest_handlers import digest_router
from content.handlers.settings_handlers import settings_router


async def main():
    dp.include_router(general_router)
    dp.include_router(digest_router)
    dp.include_router(settings_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
