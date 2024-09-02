import requests
from datetime import datetime, timedelta
import os
from db_client import DBClient

def get_transactions(token_address: str) -> str:
    url = "https://api.etherscan.io/api"
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': token_address,
        'startblock': 0,
        'endblock': 'latest',        
        'sort': 'desc',
        'apikey': os.getenv('ETHERSCAN_API_KEY')
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Unexpected response from etherscan API. Details: " + response.json())
    
    return response.json()

def check_for_updates_since(since: datetime) -> list[dict]:
    updates = []

    db_client = DBClient()
    addresses = db_client.read_addresses()
    token_address = db_client.read_token_address()

    if len(addresses) == 0:
        raise Exception("Not tracking any addresses")
    
    if token_address == "":
        raise Exception("Token Address is empty")
    
    transactions = get_transactions(token_address)

    if len(transactions) == 0:
        raise Exception("Etherscan API returned 0 transactions for the token its tracking.")

    # loop through all tansactions for token
    for tx in transactions.get('result', []):
        # break once they are older then
        if is_older_then(tx['timeStamp'], since):
            break

        # see if tx address is in our list of addresses were monitoring
        #address_in_list = next((address for address in addresses if address['address'].lower() == tx['from'].lower()), None)
        #if address_in_list != None:
        if True:
            # if there is a name provided, replace address with name so its readable
            #if address_in_list['name'] != '':
            #    tx['from'] = address_in_list['name']
            updates.append(tx)
    
    db_client.update_last_checked(since.timestamp())
    return updates


def is_older_then(timestamp: str, since: datetime) -> bool:
    timestamp = datetime.fromtimestamp(int(timestamp))
    if timestamp <= since:
        return True
    return False

