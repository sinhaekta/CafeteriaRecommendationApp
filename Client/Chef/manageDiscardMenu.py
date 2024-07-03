import json
from client import client_connection

class ManageDiscardMenu:
    def __init__(self):
        pass

    def manage_discard_menu(self):
        try:
            
            request_data = {"path": "view_discard_menu"}
            request_json = json.dumps(request_data)
            response = client_connection(request_json)

            if response:
                response = response.replace('\\"', '"')

                if response.startswith('"') and response.endswith('"'):
                            response = response.strip('"')       

                print("Response from server:", response) 
                response_data = json.loads(response)

                if isinstance(response_data, list):  
                    print("Discard Menu:")
                    for item in response_data:
                        print(f"Discard ID: {item['discard_id']}, Item ID: {item['item_id']}, Item Name: {item['item_name']}, Rating: {item['rating_value']}")

                    item_id = int(input("Enter the Item ID to manage: "))
                    action = input("Enter 'd' to delete the item or 'n' to send notification: ").strip().lower()

                    if action == 'd':
                        self.delete_item(item_id)
                    elif action == 'n':
                        self.send_notification(item_id)
                    else:
                        print("Invalid action. Please try again.")
                else:
                    print("Response data is not in expected format (list).")
            else:
                print("Empty response received from server.")

        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        except Exception as e:
            print(f"Error occurred during request: {e}")

    def delete_item(self, item_id):
        try:
            request_data = {"path": "delete_discard_item", "item_id": item_id}
            request_json = json.dumps(request_data)
            response = client_connection(request_json)

            if response:
                response_data = json.loads(response)
                print("Response:", response_data)
            else:
                print("Empty response received from server.")
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        except Exception as e:
            print(f"Error occurred during request: {e}")

    def send_notification(self, item_id):
        try:
            request_data = {"path": "send_feedback_notification", "item_id": item_id}
            request_json = json.dumps(request_data)
            response = client_connection(request_json)

            if response:
                response_data = json.loads(response)
                print("Response:", response_data)
            else:
                print("Empty response received from server.")
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        except Exception as e:
            print(f"Error occurred during request: {e}")