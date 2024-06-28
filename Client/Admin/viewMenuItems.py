import json
from client import client_connection  
from tabulate import tabulate

class ViewMenu:
    def __init__(self):
        pass
    
    def view_menu_items(self):
        request_data = {
            "path": "view_menu_items"
        }

        request_json = json.dumps(request_data)
        response = client_connection(request_json)
        
        if not response:
            print("Empty response received.")
            return
        
        try:
            response_data = json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {str(e)}")
            print(f"Response content: {response}")
            return
        
        if response_data.get("status") == "success":
            data = response_data.get("data", [])
            if not data:
                print("No data found in response.")
                return
            
            headers = ["Item ID", "Name", "Price", "Description", "Category", "Availability"]
            table_data = []

            for item in data:
                item_id = item.get("item_id", "")
                name = item.get("name", "")
                price = item.get("price", "")
                description = item.get("description", "")
                category = item.get("category", "")
                table_data.append([item_id, name, price, description, category])

            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print(f"Error response: {response_data.get('message', 'Unknown error')}")