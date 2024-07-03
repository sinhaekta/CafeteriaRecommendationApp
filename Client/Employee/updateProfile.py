import json
from client import client_connection

class UserProfile:
    def __init__(self):
        pass
    
    def update_profile(self):
        try:
            user_id = int(input("Enter your user ID: "))
            diet_type = input("Please select one - Vegetarian, Non Vegetarian, Eggetarian: ")
            spice_level = input("Please select your spice level - High, Medium, Low: ")
            cuisine_preference = input("What do you prefer most - North Indian, South Indian, Other: ")
            sweet_tooth = input("Do you have a sweet tooth? Yes or No: ")

            profile_data = {
                "user_id": user_id,
                "diet_type": diet_type,
                "spice_level": spice_level,
                "cuisine_preference": cuisine_preference,
                "sweet_tooth": sweet_tooth
            }

            response = self.send_profile_update(profile_data)

        except ValueError as ve:
            print(f"ValueError: {ve}. Please enter valid input.")
        except ConnectionError:
            print("ConnectionError: Failed to connect to the server. Please check your network.")
        except Exception as e:
            print(f"Error updating profile: {e}")

    def send_profile_update(self, profile_data):
        try:
            request_data = {
                "path": "update_profile",
                "profile_data": profile_data
            }

            request_json = json.dumps(request_data)
            response = client_connection(request_json)

            if response:
                response_data = json.loads(response)
                return response_data
            else:
                return {"status": "error", "message": "Empty response received from server."}

        except json.JSONDecodeError as e:
            return {"status": "error", "message": f"JSON decoding failed: {e}"}
        except ConnectionError:
            return {"status": "error", "message": "ConnectionError: Failed to connect to the server."}
        except Exception as e:
            return {"status": "error", "message": f"Error updating profile: {e}"}