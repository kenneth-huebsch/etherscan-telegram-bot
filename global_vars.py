import os
from dotenv import load_dotenv

load_dotenv()

URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"

#PEPE
TOKEN_ADDRESS = '0xA9E8aCf069C58aEc8825542845Fd754e41a9489A'
#SHIBA
#TOKEN_ADDRESS = '0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE'

# How often do we want to poll in seconds
POLL_TIME_SECONDS = 60*2
TELEGRAM_CHANNEL_ID='-1002162580750'