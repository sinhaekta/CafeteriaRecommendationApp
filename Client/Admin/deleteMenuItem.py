import json
from client import client_connection

class deleteMenu:
    
    def __init__(self):
        pass
    
    def delete_menu_item(self):
        item_id = input("Enter item ID to delete: ")

        request_data = {
            "item_id": item_id,
            "path": "delete_menu_item"
        }
        
        request_json = json.dumps(request_data) 

        response = client_connection(request_json)
        print(response)
