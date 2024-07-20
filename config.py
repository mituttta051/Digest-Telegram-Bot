# Import built-in packages
import os

# Import downloaded packages
from dotenv import load_dotenv

load_dotenv()

# Load variables from environment (.env)
BOT_TOKEN = '7018084887:AAH4IqHI-SzASDA2Mpc3YPPbi-j7Sb27n7c'

HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')
