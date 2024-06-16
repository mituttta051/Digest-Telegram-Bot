# Import built-in packages
import logging
import sqlite3

# Import downloaded packages
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Import project files
from config import BOT_TOKEN


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

conn = sqlite3.connect('resources/dbs/data.db')
cur = conn.cursor()

if not cur:
    logger.error("Doesn't connect to database")
