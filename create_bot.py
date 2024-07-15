# Import built-in packages
import logging

import pytz
# Import downloaded packages
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc, timezone

# Import project files
from config import BOT_TOKEN

from utils.databaseUtils import init_db

# Configure logging and logger instance
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('apscheduler').setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone=pytz.timezone('Europe/Moscow'))

# Configure a Telegram bot instance
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

try:
    init_db()
except:
    print('Can`t establish connection to database')
