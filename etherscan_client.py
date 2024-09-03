import requests
from datetime import datetime, timedelta
import os
from db_client import DBClient
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta

load_dotenv()

# returns all transactions for a given wallet
def get_transactions(wallet_address: str) -> str:
    url = "https://api.etherscan.io/api"
    params = {
        'module': 'account',
        'action': 'tokentx',
        'address': wallet_address,
        'startblock': 0,
        'endblock': 'latest',        
        'sort': 'desc',
        'apikey': os.getenv('ETHERSCAN_API_KEY')
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Unexpected response from etherscan API. Status Code: " + response.status_code)
    
    return response.json()

def check_for_updates() -> list[dict]:
    updates = []

    db_client = DBClient()
    addresses = db_client.read_addresses()
    tokens = db_client.read_tokens()

    if len(addresses) == 0:
        raise Exception("Not tracking any addresses")
    
    if len(tokens) == 0:
        raise Exception("Not tracking any tokens")
    
    for address in addresses:
        now = datetime.now()
        transactions = get_transactions(address['address'])

        if len(transactions) == 0:
            raise Exception("Etherscan API returned 0 transactions for: " + address['name'])

        # loop through all tansactions for token
        for tx in transactions.get('result', []):
            five_min_ago = now - timedelta(minutes=5)
            last_update = address.get("last_checked", five_min_ago.timestamp())
            if is_older_then(tx['timeStamp'], last_update):
                break

            # see if tx address is in our list of addresses were monitoring
            token_in_list = next((token for token in tokens if token['address'].lower() == tx['contractAddress'].lower()), None)
            if token_in_list != None:
                tx['token-emoji'] = token_in_list['emoji']
                updates.append(tx)
            
        db_client.update_last_checked(address['address'], now.timestamp())
        
        # sleep to prevent exceeding API limits
        time.sleep(1)
    
    return updates


def is_older_then(now_timestamp: str, since_timestamp: str) -> bool:
    now = datetime.fromtimestamp(int(now_timestamp))
    since = datetime.fromtimestamp(int(since_timestamp))
    if now <= since:
        return True
    return False

print(check_for_updates())