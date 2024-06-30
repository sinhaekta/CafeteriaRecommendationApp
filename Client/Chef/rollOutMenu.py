import config
import json
from client import client_connection

class RollMenu:
    def __init__(self):
        pass

    def get_input_from_chef(self):
        items = []
        try:
            for meal_time in ["breakfast", "lunch", "dinner"]:
                print(f"Select 2 items for {meal_time}:")
                for i in range(2):
                    try:
                        item_id = int(input(f"Enter item_id for {meal_time} item {i+1}: "))
                        item_name = input(f"Enter item_name for {meal_time} item {i+1}: ")
                        items.append({"item_id": item_id, "item_name": item_name, "item_category": meal_time})
                    except ValueError as ve:
                        print(f"Invalid input: {ve}. Please try again.")
                        return []
        except Exception as e:
            print(f"Error in get_input_from_chef: {e}")
            return []
        return items
    
    def roll_menu_item(self):
        print("Rolling out daily menu...")
        try:
            items = self.get_input_from_chef()
            if not items:
                print("Rolling menu operation aborted due to input errors.")
                return

            request_data = {
                "path": "roll_menu_item",
                "items": items
            }

            request_json = json.dumps(request_data)
            response = client_connection(request_json)

            if response:
                try:
                    response_data = json.loads(response)
                    print("Response:", response_data)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON response: {e}")
                    print(f"Response content: {response}")
            else:
                print("Empty response received from server.")
        except ConnectionError:
            print("Failed to connect to the server. Please check your network connection and try again.")
        except Exception as e:
            print("Error occurred during request:", e)