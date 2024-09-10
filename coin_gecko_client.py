import requests
import os
from dotenv import load_dotenv

load_dotenv()

URL = 'https://api.coingecko.com/api/v3/simple/token_price/ethereum?vs_currencies=usd&contract_addresses='

# returns all transactions for a given wallet
def get_price(token_address: str) -> str:
    url = URL + token_address.lower()
    headers = {'accept': 'application/json',
               'x-cg-demo-api-key': os.getenv('COIN_GECKO_API_KEY')}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Coin gecko API return status code {response.status_code}")
    return response.json().get(token_address.lower(), {}).get('usd', 0.0)

def get_total_cost(token_address: str, amount: float) -> str:
    try:
        price = get_price(token_address)
    except:
        price = 0
    value = round(price * amount, 2)
    formatted_value = "{:.2f}".format(value)
    return str(formatted_value)