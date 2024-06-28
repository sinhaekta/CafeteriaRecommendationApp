import json
from client import client_connection

class DeleteMenu:
    
    def __init__(self):
        pass
    
    def delete_menu_item(self):
        try:
            item_id = int(input("Enter item ID to delete: ")) 

            request_data = {
                "item_id": item_id,
                "path": "delete_menu_item"
            }
            
            request_json = json.dumps(request_data) 

            response = client_connection(request_json)
            print(response)
        
        except ValueError:
            print("Invalid input. Please enter a valid item ID (a positive integer).")
            
        except Exception as e:
            print(f"Error: {e}")
