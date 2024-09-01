import json

class AddressDBClient:
    def __init__(self):
        self.filepath = "./addresses.json"

    def add(self, address: dict) -> bool:
        data = self.read()
        address_in_list = next((a for a in data if a['address'].lower() == address['address'].lower()), None)
        if address_in_list != None:
            return False
        try:
            data.append(address)
            with open(self.filepath, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            return False
        
    def remove(self, name: str) -> bool:
        data = self.read()
        address_in_list = next((a for a in data if a['name'].lower() == name.lower()), None)
        if address_in_list == None:
            return False
        try:
            data.remove(address_in_list)
            with open(self.filepath, 'w') as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            return False
        
        return True
    
    def read(self) -> list[dict]:
        with open(self.filepath, 'r') as file:
            data = json.load(file)
        return data