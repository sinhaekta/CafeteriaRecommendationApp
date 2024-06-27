import json
from client import client_connection

class RollMenu:
    def __init__(self):
        pass

    def get_input_from_chef(self):
        items = []
        for meal_time in ["breakfast", "lunch", "dinner"]:
            print(f"Select 2 items for {meal_time}:")
            for i in range(2):
                item_id = int(input(f"Enter item_id for {meal_time} item {i+1}: "))
                item_name = input(f"Enter item_name for {meal_time} item {i+1}: ")
                items.append({"item_id": item_id, "item_name": item_name, "item_category": meal_time})
        return items
    
    def roll_menu_item(self):
        print("Rolling out daily menu...")
        try:
            items = self.get_input_from_chef()

            request_data = {
                "path": "roll_menu_item",
                "items": items
            }

            request_json = json.dumps(request_data)
            response = client_connection(request_json)

            if response:
                response_data = json.loads(response)
                print("Response:", response_data)
            else:
                print("Empty response received from server.")
        except Exception as e:
            print("Error occurred during request:", e)

