import Config
import json
from Client import client_connection

class DeleteMenu:
    
    def __init__(self):
        pass
    
    def delete_menu_item(self):

        attempts = Config.MAX_ATTEMPT
        
        while attempts > Config.MIN_ATTEMPT:
            try:
                item_id = int(input("Enter item ID to delete: ")) 

                if item_id <= Config.MIN_ATTEMPT:
                    raise ValueError("Item ID must be a positive integer.")

                request_data = {
                    "item_id": item_id,
                    "path": "delete_menu_item"
                }
                
                request_json = json.dumps(request_data) 

                response = client_connection(request_json)
                response_data = json.loads(response)
                
                if response_data.get('status') == 'success':
                    print(f"Item with ID {item_id} deleted successfully.")
                else:
                    print(f"Failed to delete item: {response_data.get('error', 'Unknown error')}")
                break
            
            except ValueError as ve:
                print(f"Invalid input: {ve}. Please enter a valid item ID (a positive integer).")
                attempts -= 1
                if attempts > Config.MIN_ATTEMPT:
                    print(f"You have {attempts} more attempt(s).")
            
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