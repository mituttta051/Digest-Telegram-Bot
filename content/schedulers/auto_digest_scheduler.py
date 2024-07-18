# Import built-in packages
from datetime import datetime, timedelta  # Todo: Remove unused import
from typing import Union

# Import downloaded packages
import pytz
from apscheduler.triggers.date import DateTrigger
from croniter import croniter
from pytz import timezone, utc  # Todo: Use importing of individual methods

# Import project files
from create_bot import scheduler, bot
from utils.LLMUtils import generate_summary
from utils.botUtils import get_messages_in_days
from utils.databaseUtils import get_channels


def update_scheduler() -> None:
    channels = get_channels()
    for channel_id, name, main_l, additional_l, auto_digest, auto_digest_date, __, ___ in channels:
        channel_id = str(channel_id)
        if auto_digest == "yes":
            schedule(channel_id, auto_digest_date)
        else:
            if scheduler.get_job(channel_id) is not None:
                scheduler.remove_job(channel_id)


def schedule(channel_id: Union[str, int], auto_digest_date: str) -> None:
    scheduler.add_job(
        func=schedule_function,
        id=channel_id,
        replace_existing=True,
        kwargs={
            "channel_id": channel_id,
            "auto_digest_date": auto_digest_date
        },
        trigger=DateTrigger(
            run_date=croniter(auto_digest_date, datetime.now(tz=pytz.timezone('Europe/Moscow'))).get_next(datetime)),
        timezone=pytz.timezone('Europe/Moscow'),
        misfire_grace_time=42,
    )


async def schedule_function(channel_id: Union[str, int], auto_digest_date: str) -> None:
    # Get the latest messages within the specified period
    messages = get_messages_in_days(channel_id, "7")  # Todo: Rework. Does period should be const value?
    if len(messages) != 0:
        digest = await generate_summary(messages, channel_id, None)

        await bot.send_message(chat_id=channel_id, text=digest)
    scheduler.add_job(
        func=schedule_function,
        id=channel_id,
        replace_existing=True,
        kwargs={
            "channel_id": channel_id,
            "auto_digest_date": auto_digest_date
        },
        trigger=DateTrigger(run_date=croniter(auto_digest_date, datetime.now()).get_next(datetime)),
        timezone=pytz.timezone('Europe/Moscow')
    )
