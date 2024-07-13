# Import built-in packages
import logging

# Import downloaded packages
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

# Import project files
from config import BOT_TOKEN

from utils.databaseUtils import init_db

# Configure logging and logger instance
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure a Telegram bot instance
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

try:
    init_db()
except:
    print('Can`t establish connection to database')
