from datetime import datetime, timedelta

from apscheduler.triggers.date import DateTrigger
from croniter import croniter
from pytz import timezone, utc

from create_bot import scheduler, bot
from utils.LLMUtils import generate_summary
from utils.botUtils import get_messages_in_days
from utils.databaseUtils import get_channels


def update_scheduler():
    channels = get_channels()
    for _, channel_id, name, main_l, additional_l, auto_digest, auto_digest_date in channels:
        channel_id = str(channel_id)
        if auto_digest == "yes":
            schedule(channel_id, auto_digest_date)
        else:
            if scheduler.get_job(channel_id) is not None:
                scheduler.remove_job(channel_id)


def schedule(channel_id, auto_digest_date):
    scheduler.add_job(
        func=schedule_function,
        id=channel_id,
        replace_existing=True,
        kwargs={
            "channel_id": channel_id,
            "auto_digest_date": auto_digest_date
        },
        trigger=DateTrigger(run_date=croniter(auto_digest_date, datetime.now()).get_next(datetime)),
        timezone=utc,
        misfire_grace_time=42,
    )


async def schedule_function(channel_id, auto_digest_date):
    # Get the latest messages within the specified period
    messages = get_messages_in_days(channel_id, "7")
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
        trigger=DateTrigger(run_date=croniter(auto_digest_date, datetime.now()).get_next(datetime))
    )
