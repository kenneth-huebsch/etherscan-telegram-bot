import requests
from datetime import datetime
import os

URL = f"https://api.telegram.org/bot{os.environ('TELEGRAM_BOT_TOKEN')}/sendMessage"

def format_readable(updates: list[dict]) -> str:
    ret_val = ""
    for tx in updates:
        ret_val +=  str(tx['from']) + ' sent to ' + str(tx['to']) \
                  + ' on ' + datetime.fromtimestamp(int(tx['timeStamp'])).strftime('%b-%d at %H:%M') + '\n'
        ret_val += 'For more info: https://etherscan.io/tx/' + tx['hash'] + '\n\n'
    return ret_val


def send_message_to_channel(updates: list[dict]):
    # Data to be sent to the API
    data = {
        'chat_id': os.environ('TELEGRAM_CHANNEL_ID'),
        'text': format_readable(updates)
    }
    print(format_readable(updates))   
    
    response = requests.post(URL, data=data)

    # Checking the response
    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print(f'Failed to send message: {response.text}')