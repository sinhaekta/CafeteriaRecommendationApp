import json
from client import client_connection

class UpdateMenu:
    
    def __init__(self):
        pass
    
    def update_menu_item(self):
        try:
            item_id = int(input("Enter item ID to update: "))  
            name = input("Enter new item name: ")
            price = float(input("Enter new item price: ")) 
            description = input("Enter new item description: ")
            category = input("Enter item category (breakfast, lunch, dinner, all day): ")

            request_data = {
                "item_id": item_id,
                "name": name,
                "price": price,
                "description": description,
                "category": category,
                "path": "update_menu_item"
            }
            
            request_json = json.dumps(request_data) 

            response = client_connection(request_json)
            print(response)
        
        except ValueError as ve:
            print(f"Input error: {ve}")

        except Exception as e:
            print(f"Error: {e}")


