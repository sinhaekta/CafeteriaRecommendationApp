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
                response_data = json.loads(response)
                print("Response:", response_data)
            else:
                print("Empty response received from server.")
        
        except Exception as e:
            print("Error occurred during request:", e)
