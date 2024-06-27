import json
from client import client_connection

class Notification:
    def __init__(self):
        pass
    
    def check_notification(self):
        try:
            request_data = {
                "path": "check_notification"
            }

            request_json = json.dumps(request_data)
            response = client_connection(request_json)

            if response:
                response_data = json.loads(response)
                if response_data["status"] == "success":
                    notifications = response_data["data"]
                    print("Notifications:")
                    for notification in notifications:
                        print(f"Notification ID: {notification['notification_id']}")
                        print(f"Message: {notification['message']}")
                        print(f"Date: {notification['notification_date']}")
                        print("------------")
                else:
                    print(f"Error: {response_data['message']}")
            else:
                print("Empty response received from server.")
        
        except Exception as e:
            print("Error occurred during request:", e)

