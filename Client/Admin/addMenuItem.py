import json
from client import client_connection

class AddMenu:
    
    def __init__(self):
        pass
    
    def add_menu_item(self):
        name = input("Enter item name: ")
        price = input("Enter item price: ")
        description = input("Enter item description: ")
        category = input("Enter item category (breakfast, lunch, dinner, all day): ")

        request_data = {
            "name": name,
            "price": price,
            "description": description,
            "category": category,
            "path": "add_menu_item"
        }
        
        request_json = json.dumps(request_data) 

        response = client_connection(request_json)
        print(response)