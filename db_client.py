import json
import threading

class DBClient:
    def __init__(self):
        self.filepath = "./db.json"
        self.file_lock = threading.Lock()

    def read(self) -> dict:
        with self.file_lock:        
            with open(self.filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        return data
    
    def write(self, data: dict) -> bool:
        try:
            with self.file_lock:
                with open(self.filepath, 'w', encoding='utf-8') as file:
                    json.dump(data, file, indent=4)
        except Exception as e:
            return False
        return True              

    def read_tokens(self) -> list[dict]:
        data = self.read()
        return data['tokens']
    
    def add_token(self, new_token: dict) -> bool:
        data = self.read()
        token_in_list = next((token for token in data['tokens'] if token['address'].lower() == new_token['address'].lower()), None)
        if token_in_list != None:
            return False
        data['tokens'].append(new_token)
        return self.write(data)

    def remove_token(self, address: str) -> bool:
        data = self.read()
        token_in_list = next((token for token in data['tokens'] if token['address'].lower() == address.lower()), None)
        if token_in_list == None:
            return False
        data['tokens'].remove(token_in_list)
        return self.write(data)
              
    def read_token_emoji(self, address: str) -> str:
        data = self.read()
        token_in_list = next((token for token in data['tokens'] if token['address'].lower() == address.lower()), None)
        return token_in_list['emoji']       
            
    def read_last_checked(self) -> str:
        data = self.read()
        addresses = data.get(addresses)
        if len(addresses) > 0:
            last_checked = addresses[0].get('last_checked')
        return last_checked

    def update_last_checked(self, address: str, timestamp: str) -> bool:
        data = self.read()
        address_in_list = next((a for a in data['addresses'] if a['address'].lower() == address.lower()), None)
        if address_in_list != None:
            address_in_list['last_checked'] = timestamp
        return self.write(data)

    def add_address(self, address: dict) -> bool:
        data = self.read()
        address_in_list = next((a for a in data['addresses'] if a['name'].lower() == address['name'].lower()), None)
        if address_in_list != None:
            return False
        data['addresses'].append(address)
        return self.write(data)

    def remove_address(self, name: str) -> bool:
        data = self.read()
        address_in_list = next((a for a in data['addresses'] if a['name'].lower() == name.lower()), None)
        if address_in_list == None:
            return False
        data['addresses'].remove(address_in_list)
        return self.write(data)
    
    def read_addresses(self) -> list[dict]:
        return self.read()['addresses']