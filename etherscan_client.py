import requests
from datetime import datetime, timedelta
import os

def get_transactions(token_address: str) -> str:
    url = "https://api.etherscan.io/api"
    params = {
        'module': 'account',
        'action': 'txlist',
        'address': token_address,
        'startblock': 0,
        'endblock': 'latest',        
        'sort': 'desc',
        'apikey': os.environ('ETHERSCAN_API_KEY')
    }
    response = requests.get(url, params=params)
    return response.json()

def check_for_updates_since(addresses: list[str], token_address: str, since: datetime) -> list[dict]:
    updates = []
    
    transactions = get_transactions(token_address)

    # loop through all tansactions for token
    for tx in transactions.get('result', []):

        # break once they are older then
        if isOlderThen(tx['timeStamp'], since):
            break

        # filter on addresses
        if tx['from'] in addresses:
            updates.append(tx)
    
    return updates


def isOlderThen(timestamp: str, since: datetime) -> bool:
    timestamp = datetime.fromtimestamp(int(timestamp))
    if timestamp <= since:
        return True
    return False

