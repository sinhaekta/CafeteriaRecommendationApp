import json
from client import client_connection

class FoodOrder:
    def __init__(self):
        pass
    
    def order_food(self):
        try:
            user_id = int(input("Enter your user ID: "))
            breakfast_item_id = int(input("Enter the item ID for breakfast: "))
            lunch_item_id = int(input("Enter the item ID for lunch: "))
            dinner_item_id = int(input("Enter the item ID for dinner: "))
            
            request_data = {
                "path": "order_food",
                "user_id": user_id,
                "breakfast_item_id": breakfast_item_id,
                "lunch_item_id": lunch_item_id,
                "dinner_item_id": dinner_item_id
            }

            request_json = json.dumps(request_data)
            response = client_connection(request_json)

            if response:
                if response.startswith('"') and response.endswith('"'):
                    response = response.strip('"')

                try:
                    response_data = json.loads(response)
                    print("Received Data:", response_data)
                    print("Type of Received Data:", type(response_data)) 

                    if response_data.get("status") == "success":
                        print("Order placed successfully")
                    else:
                        print("Failed to place order:", response_data.get("message"))

                except json.JSONDecodeError as e:
                    print("JSON decoding failed:", e)
            else:
                print("Empty response received from server.")

        except ValueError as ve:
            print(f"ValueError: {ve}. Please enter valid integer IDs.")
        except ConnectionError:
            print("ConnectionError: Failed to connect to the server. Please check your network.")
        except Exception as e:
            print(f"Error occurred: {e}")