# Import downloaded packages
import asyncio

# Import project files
from create_bot import bot, dp
from content.handlers.general_handlers import general_router
from content.handlers.digest_handlers import digest_router
from content.handlers.settings_handlers import settings_router


async def main():
    """
        Asynchronous main function to initialize and start the Telegram bot.

        This function includes routers for handling different types of commands and messages,
        deletes the bot's webhook to allow polling, and starts the polling mechanism to receive updates.
    """
    # Include routers in the dispatcher
    dp.include_router(general_router)  # Include general router
    dp.include_router(digest_router)  # Include digest router
    dp.include_router(settings_router)  # Include settings router

    # Delete the bot's webhook and allow polling for updates
    await bot.delete_webhook(drop_pending_updates=True)

    # Start polling to receive updates
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
