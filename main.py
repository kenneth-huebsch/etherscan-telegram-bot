import etherscan_client
import telegram_client
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Enter address that we want to keep track of
ADDRESSES = ['0xFb2dD1bCc3927b8fdcC476565d58e80BBB107e9A', '0x01d678a376427f23Ab44dFdF82e6Ad65025c19BD']

# Enter tokens that we want to keep track of
TOKEN_ADDRESS = '0xA9E8aCf069C58aEc8825542845Fd754e41a9489A'
#SHIBA TOKEN_ADDRESS = '0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE'

# How often do we want to poll in seconds
POLL_TIME_SECONDS = 60*2

# state the bot
print("Starting Etherscan bot...")
load_dotenv()

# loop every POLL_TIME_SECONDS
last_check = datetime.now() - timedelta(seconds=POLL_TIME_SECONDS)
while(1):
    updates = etherscan_client.check_for_updates_since(ADDRESSES, TOKEN_ADDRESS, last_check)
    last_check = datetime.now()
    if len(updates) > 0:
        telegram_client.send_message_to_channel(updates)

    time.sleep(POLL_TIME_SECONDS)
