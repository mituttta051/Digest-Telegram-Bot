# Import built-in packages
import os

# Import downloaded packages
from dotenv import load_dotenv

load_dotenv()

# Load variables from environment (.env)
BOT_TOKEN = os.getenv('BOT_TOKEN')
YGPT_FOLDER_ID = os.getenv('YGPT_FOLDER_ID')
YGPT_TOKEN = os.getenv('YGPT_TOKEN')
