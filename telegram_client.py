import requests
from datetime import datetime
import os
import telebot
import global_vars
from db_client import DBClient

bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

@bot.channel_post_handler(commands=['add'])
def handle_add_command(message):
    # Split the message text to get command and parameter
    parts = message.text.split(maxsplit=2)
    response = ''
    if len(parts) == 3:
        if parts[2][:2] != "0x":
            response = "Expected /add <name> <address>"
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
        # Inform the user that they need to provide a parameter
        response = "Please provide a value to add. Usage: /add <name> <address>"
    
    bot.reply_to(message, response)

@bot.channel_post_handler(commands=['token'])
def handle_token_command(message):
    db_client = DBClient()
    address = db_client.read_token_address()
    emoji = db_client.read_token_emoji()
    reply = "Tracking: " + emoji +  " - " + address
    bot.reply_to(message, reply)

@bot.channel_post_handler(commands=['update-token'])
def handle_update_token_command(message):
    # Split the message text to get command and parameter
    parts = message.text.split(maxsplit=2)
    response = ''
    if len(parts) == 3:
        if parts[1][:2] != "0x":
            response = "Expected /update-token <address> <emoji>"
        else:
            data = {}
            data['address'] = parts[1]            
            data['emoji'] = parts[2]
            db_client = DBClient()
            success = db_client.update_token(data)
            if success == False:
                response = "Unable to update token."
            else:
                address = db_client.read_token_address()
                emoji = db_client.read_token_emoji()
                response = "Tracking: " + emoji +  " - " + address
    else:
        # Inform the user that they need to provide a parameter
        response = "Please provide a value to add. Usage: /add <name> <address>"
    
    bot.reply_to(message, response)

@bot.channel_post_handler(commands=['remove'])
def handle_remove_command(message):
    # Split the message text to get command and parameter
    parts = message.text.split(maxsplit=1)
    response = ''

    if len(parts) == 2:
        if parts[1][:2] == "0x":
            response = "Expected /remove <name>"
        else:
            db_client = DBClient()
            success = db_client.remove_address(parts[1])
            if success == False:
                response = "Unable to remove address. Maybe there isn't any record with that name?"
            else:
                all_addresses = db_client.read_addresses()
                response = format_addresses(all_addresses)
    else:
        # Inform the user that they need to provide a parameter
        response = "Please provide a value to remove. Usage: /remove <name>"
    
    bot.reply_to(message, response)

@bot.channel_post_handler(commands=['addresses'])
def handle_addresses_command(message):
    db_client = DBClient()
    addresses = db_client.read_addresses()
    bot.reply_to(message, format_addresses(addresses))

@bot.channel_post_handler(commands=['status'])
def handle_status_command(message):
    db_client = DBClient()
    last_checked = db_client.read_last_checked()
    message = "Etherscan last checked: " + datetime.fromtimestamp(last_checked).strftime('%Y-%m-%d %H:%M:%S')
    with open('./im-alive.gif', 'rb') as file:
            bot.send_animation(chat_id=global_vars.TELEGRAM_CHANNEL_ID, animation=file, caption=message)

@bot.channel_post_handler(commands=['help'])
def handle_help_command(message):
    reply =   "/status - Returns whether or not bot is alive\n" \
            + "/addresses - Returns a list of addresses currently being tracked\n" \
            + "/add <name> <address> - Adds an address to the list of addresses being tracked\n" \
            + "/remove <name> - Removes an address from the list of addresses being tracked\n" \
            + "/token - Returns the token being tracked\n" \
            + "/update-token <token-address> <emoji-unicode> - Updates the token being tracked\n" \
            + "/help = Prints this info\n"
    bot.reply_to(message, reply)

def send_start_message():
    db_client = DBClient()
    addresses = db_client.read_addresses()
    message = '\U0001F44B - Etherscan Bot Up and running!\nTracking the following addresses:\n' \
            + format_addresses(addresses)
    send_message_to_channel(message)

def start_bot():
    bot.infinity_polling()

def format_addresses(addresses: list[dict]) -> str:
    ret_val = ""
    for address in addresses:
        ret_val += address['name'] + ': ' + address['address'][:16] + '...\n'
    return ret_val

def format_updates(updates: list[dict]) -> str:
    ret_val = ""
    db_client = DBClient()
    emoji = db_client.read_token_emoji()
    for tx in updates:
        ret_val +=  '\U0001F911 - ' + tx['from'] + ' sent ' + emoji \
                  + ' on ' + datetime.fromtimestamp(int(tx['timeStamp'])).strftime('%b-%d at %H:%M') + ' '
        ret_val += '<a href="https://etherscan.io/tx/' + tx['hash'] + '">Etherscan Link</a>\n\n'
    return ret_val

def send_message_to_channel(message: str):
    data = {
        'chat_id': global_vars.TELEGRAM_CHANNEL_ID,
        'text': message,
        'parse_mode': 'HTML'
    }    
    response = requests.post(global_vars.URL, data=data)

def send_updates_to_channel(updates: list[dict]):
    # Data to be sent to the API
    data = {
        'chat_id': global_vars.TELEGRAM_CHANNEL_ID,
        'text': format_updates(updates),
        'parse_mode': 'HTML'
    }
    response = requests.post(global_vars.URL, data=data)

    # Checking the response
    if response.status_code != 200:
        print(f'Failed to send message: {response.text}')