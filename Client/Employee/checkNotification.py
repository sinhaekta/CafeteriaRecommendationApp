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
                try:
                    response_data = json.loads(response)
                    if isinstance(response_data, dict):
                        if response_data["status"] == "success":
                            notifications = response_data.get("data", [])
                            if notifications:
                                for notification in notifications:
                                    print("Notification:")
                                    print(f"Notification ID: {notification.get('notification_id', '')}")
                                    print(f"Message: {notification.get('message', '')}")
                                    print(f"Notification Date: {notification.get('notification_date', '')}")
                                    print("------------")
                            else:
                                print("No notifications found.")
                        else:
                            print(f"Error: {response_data.get('message', 'Unknown error')}")
                    else:
                        print(f"Invalid response format: {response_data}")

                except json.JSONDecodeError as e:
                    print(f"JSON decoding failed: {e}")
                    print(f"Response content: {response}") 
            else:
                print("Empty response received from server.")

        except ConnectionError:
            print("Failed to connect to the server. Please check your network connection and try again.")
        except Exception as e:
            print(f"Error occurred during request: {e}")

