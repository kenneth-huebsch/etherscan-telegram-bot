import os
from dotenv import load_dotenv

load_dotenv()

URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
TELEGRAM_CHANNEL_ID='-1002162580750'