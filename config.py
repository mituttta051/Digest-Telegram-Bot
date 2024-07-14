# Import built-in packages
import os

# Import downloaded packages
from dotenv import load_dotenv

load_dotenv()

# Load variables from environment (.env)
BOT_TOKEN = os.getenv('BOT_TOKEN')

HUGGING_FACE_TOKEN = os.getenv('HUGGING_FACE_TOKEN')
