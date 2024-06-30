import json
from client import client_connection

class DiscardFeedback:
    
    def __init__(self):
        pass
    
    def view_discard_item_notifications(self):
        try:
            request_data = {
                "path": "fetch_discard_item_notifications"
            }
            request_json = json.dumps(request_data)
            response = client_connection(request_json)

            if response:
                response_data = json.loads(response)
                if response_data['status'] == 'success':
                    notifications = response_data['data']
                    for notification in notifications:
                        print(f"Notification ID: {notification['notification_id']}")
                        print(f"Item ID: {notification['item_id']}")
                        print(f"Message: {notification['message']}")
                        print(f"Notification Date: {notification['notification_date']}")
                        print()

                    if notifications:
                        self.give_feedback_discard_item(notifications)
                    else:
                        print("No discard item notifications found.")
                else:
                    print(f"Error: {response_data['message']}")
            else:
                print("Empty response received from server.")

        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        except Exception as e:
            print(f"Error occurred during request: {e}")

    def give_feedback_discard_item(self, notifications):
        try:
            notification_id = int(input("Enter the Notification ID for feedback: "))
            feedback = input("Enter your feedback: ")

            for notification in notifications:
                if notification['notification_id'] == notification_id:
                    user_id = int(input("Enter your user ID: "))
                    request_data = {
                        "path": "give_feedback_discard_item",
                        "user_id": user_id,
                        "notification_id": notification_id,
                        "feedback": feedback
                    }
                    request_json = json.dumps(request_data)
                    response = client_connection(request_json)

                    if response:
                        response_data = json.loads(response)
                        print("Response:", response_data)
                    else:
                        print("Empty response received from server.")
                    break
            else:
                print(f"Notification ID {notification_id} not found.")

        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
        except Exception as e:
            print(f"Error occurred during request: {e}")
