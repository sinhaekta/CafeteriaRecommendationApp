import json
from client import client_connection

class Notification:
    def __init__(self):
        pass
    
    def send_notification(self):
        try:
            request_data = {
                "path": "send_notification"
            }

            request_json = json.dumps(request_data)
            response = client_connection(request_json)

            if response:
                try:
                    response_data = json.loads(response)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON response: {e}")
            else:
                print("Empty response received from server.")
        
        except ConnectionError:
            print("Failed to connect to the server. Please check your network connection and try again.")
        except Exception as e:
            print("Error occurred during request:", e)