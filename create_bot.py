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

# Configure logging and logger instance
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure a Telegram bot instance
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

# Initialize database connection
conn = sqlite3.connect('resources/dbs/data.db')
cur = conn.cursor()

if not cur:  # In case of connection error (not exist, wrong path, ...)
    logger.error("Doesn't connect to database")
