import json

class DBClient:
    def __init__(self):
        self.filepath = "./db.json"

    def read_token_address(self) -> str:
        data = self.read()
        return data['token']['address']
    
    def update_token(self, address_dict: dict) -> bool:
        data = self.read()
        data['token'] = address_dict
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)        
        except Exception as e:
            return False
            
    def read_token_emoji(self) -> str:
        data = self.read()
        return data['token']['emoji']        
            
    def read_last_checked(self) -> str:
        data = self.read()
        return data['last_checked']

    def update_last_checked(self, timestamp: str) -> bool:
        data = self.read()
        data['last_checked'] = timestamp
        try:
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)        
        except Exception as e:
            return False

    def add_address(self, address: dict) -> bool:
        data = self.read()
        address_in_list = next((a for a in data['addresses'] if a['name'].lower() == address['name'].lower()), None)
        if address_in_list != None:
            return False
        try:
            data['addresses'].append(address)
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            return False
        
    def remove_address(self, name: str) -> bool:
        data = self.read()
        address_in_list = next((a for a in data['addresses'] if a['name'].lower() == name.lower()), None)
        if address_in_list == None:
            return False
        try:
            data['addresses'].remove(address_in_list)
            with open(self.filepath, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            return False
        
        return True
    
    def read(self) -> dict:
        with open(self.filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    
    def read_addresses(self) -> list[dict]:
        return self.read()['addresses']