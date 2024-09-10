import requests
from datetime import datetime
import os
import telebot
from db_client import DBClient
from dotenv import load_dotenv
import coin_gecko_client

load_dotenv()
BOT = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))
URL = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')

db_client = DBClient()

@BOT.channel_post_handler(commands=['add-address'])
def handle_add_address_command(message):
    parts = message.text.split(maxsplit=2)
    if len(parts) == 3:
        if parts[2][:2] != "0x":
            response = "Expected /add-address <name> <address>"
        else:
            data = {}
            data['name'] = parts[1]            
            data['address'] = parts[2]
            db_client = DBClient()
            success = db_client.add_address(data)
            if success == False:
                response = "Unable to add address. Maybe a record with the same name already exists?"
            else:
                all_addresses = db_client.read_addresses()
                response = format_addresses(all_addresses)
    else:
        response = "Please provide a value to add. Usage: /add-address <name> <address>"
    BOT.reply_to(message, response)

@BOT.channel_post_handler(commands=['tokens'])
def handle_tokens_command(message):
    tokens = db_client.read_tokens()
    reply = "Tracking:\n" + format_tokens(tokens)
    BOT.reply_to(message, reply)

@BOT.channel_post_handler(commands=['add-token'])
def handle_add_token_command(message):
    parts = message.text.split(maxsplit=2)
    if len(parts) == 3:
        if parts[2][:2] != "0x":
            response = "Expected /add-token <emoji> <address>"
        else:
            data = {}
            data['emoji'] = parts[1]            
            data['address'] = parts[2]            
            success = db_client.add_token(data)
            if success == False:
                response = "Unable to add token."
            else:
                tokens = db_client.read_tokens()
                response = "Tracking:\n" + format_tokens(tokens)
    else:
        response = "Please provide a value to add. Usage: /add-token <name> <address>"
    
    BOT.reply_to(message, response)

@BOT.channel_post_handler(commands=['remove-token'])
def handle_remove_token_command(message):
    parts = message.text.split(maxsplit=1)
    response = ''
    if len(parts) == 2:
        if parts[1][:2] != "0x":
            response = "Expected /remove-token <address>"
        else:
            success = db_client.remove_token(parts[1])
            if success == False:
                response = "Unable to remove token. Maybe there isn't any record with that address?"
            else:
                all_tokens = db_client.read_tokens()
                response = format_tokens(all_tokens)
    else:
        response = "Please provide a value to remove. Usage: /remove-token <address>"
    
    BOT.reply_to(message, response)

@BOT.channel_post_handler(commands=['remove-address'])
def handle_remove_address_command(message):
    parts = message.text.split(maxsplit=1)
    response = ''
    if len(parts) == 2:
        if parts[1][:2] == "0x":
            response = "Expected /remove-address <name>"
        else:
            success = db_client.remove_address(parts[1])
            if success == False:
                response = "Unable to remove address. Maybe there isn't any record with that name?"
            else:
                all_addresses = db_client.read_addresses()
                response = format_addresses(all_addresses)
    else:
        response = "Please provide a value to remove. Usage: /remove-token <name>"
    
    BOT.reply_to(message, response)

@BOT.channel_post_handler(commands=['addresses'])
def handle_addresses_command(message):
    addresses = db_client.read_addresses()
    BOT.reply_to(message, format_addresses(addresses))

@BOT.channel_post_handler(commands=['status'])
def handle_status_command(message):
    last_checked = db_client.read_last_checked()
    message = "Etherscan last checked: " + datetime.fromtimestamp(last_checked).strftime('%Y-%m-%d %H:%M:%S')
    with open('./im-alive.gif', 'rb') as file:
            BOT.send_animation(chat_id=TELEGRAM_CHANNEL_ID, animation=file, caption=message)

@BOT.channel_post_handler(commands=['help'])
def handle_help_command(message):
    reply =   "/status - Returns whether or not bot is alive\n" \
            + "/addresses - Returns a list of addresses currently being tracked\n" \
            + "/add-address <name> <address> - Adds an address to the list of addresses being tracked\n" \
            + "/remove-address <name> - Removes an address from the list of addresses being tracked\n" \
            + "/tokens - Returns the tokens being tracked\n" \
            + "/add-token <emoji> <token-address>  - Adds a token to track\n" \
            + "/remove-token <address> - Removes a token from the list of tokens being tracked\n" \
            + "/help = Prints this info\n"
    BOT.reply_to(message, reply)

def send_start_message():
    addresses = db_client.read_addresses()
    message = '\U0001F44B - Etherscan Bot Up and running!\nTracking the following addresses:\n' \
            + format_addresses(addresses)
    send_message_to_channel(message)

def start_bot():
    BOT.infinity_polling()

def format_addresses(addresses: list[dict]) -> str:
    ret_val = ""
    for address in addresses:
        ret_val += address['name'] + ': ' + address['address'] + '\n'
    return ret_val

def format_tokens(tokens: list[dict]) -> str:
    ret_val = ""
    for token in tokens:
        ret_val += token['emoji'] + ' - ' + token['address'] + '\n'
    return ret_val

def format_updates(updates: list[dict]) -> str:
    ret_val = ""
    for tx in updates:
        token_decimal = -1 * int(tx.get('tokenDecimal', '18'))
        amount = float(tx['value'][:token_decimal] + '.' + tx['value'][token_decimal:])
        cash_value = coin_gecko_client.get_total_cost(tx['contractAddress'], amount)
        ret_val +=  'SELL - ' + tx['token-emoji'] + ' - ' + db_client.get_name_from_address(tx['from']) + '\n' \
                + 'from: ' + tx['from'] + '\n' \
                + 'to: ' + tx['to']  + '\n' \
                + 'amount: ' + str(amount) + '\n' \
                + 'value: $' + cash_value + '\n' \
                + '<a href="https://etherscan.io/tx/' + tx['hash'] + '">Etherscan Link</a>\n\n'
    return ret_val

def send_message_to_channel(message: str):
    data = {
        'chat_id': TELEGRAM_CHANNEL_ID,
        'text': message,
        'parse_mode': 'HTML'
    }    
    response = requests.post(URL, data=data)

def send_updates_to_channel(updates: list[dict]):
    # Data to be sent to the API
    data = {
        'chat_id': TELEGRAM_CHANNEL_ID,
        'text': format_updates(updates),
        'parse_mode': 'HTML',
        'disable_web_page_preview': 'true'
    }
    response = requests.post(URL, data=data)

    # Checking the response
    if response.status_code != 200:
        print(f'Failed to send message: {response.text}')