import Config
import json
from Client import client_connection

class UpdateMenu:
    
    def __init__(self):
        pass
    
    def update_menu_item(self):
        attempts = Config.MAX_ATTEMPT
        
        while attempts > Config.MIN_ATTEMPT:
            try:
                item_id = int(input("Enter item ID to update: "))  
                if item_id <= Config.MIN_ATTEMPT:
                    raise ValueError("Item ID must be a positive integer.")
                
                name = input("Enter new item name: ").strip()
                if not name:
                    raise ValueError("Item name cannot be empty.")
                
                price = float(input("Enter new item price: "))
                if price <= Config.MIN_ATTEMPT:
                    raise ValueError("Price must be a positive number.")
                
                description = input("Enter new item description: ").strip()
                if not description:
                    raise ValueError("Description cannot be empty.")
                
                category = input("Enter item category (breakfast, lunch, dinner, all day): ").strip().lower()
                valid_categories = {"breakfast", "lunch", "dinner", "all day"}
                if category not in valid_categories:
                    raise ValueError("Invalid category. Valid categories are: breakfast, lunch, dinner, all day.")

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
                response_data = json.loads(response)

                if response_data.get('status') == 'success':
                    print(f"Item with ID {item_id} updated successfully.")
                else:
                    print(f"Failed to update item: {response_data.get('error', 'Unknown error')}")
                break
            
            except ValueError as ve:
                print(f"Input error: {ve}")
                attempts -= 1
                if attempts > Config.MIN_ATTEMPT:
                    print(f"You have {attempts} more attempt(s). Please try again.")
            
            except json.JSONDecodeError:
                print("Failed to decode the server response. Please try again.")
                break
            
            except ConnectionError:
                print("Failed to connect to the server. Please check your network connection and try again.")
                break
            
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                break

        if attempts == Config.MIN_ATTEMPT:
            print("You have exceeded maximum attempts. Please try later")