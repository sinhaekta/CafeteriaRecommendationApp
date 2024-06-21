import json
from client import client_connection  
class recommendation:
    def __init__(self):
        pass
    
    def view_recommendation(self):
        try:
            request_data = {
                "path": "view_recommended_menu"
            }

            request_json = json.dumps(request_data)
            print("Request JSON:", request_json)  
            response = client_connection(request_json)
            print("Response:", response)  

            if response:
                response_data = json.loads(response)
                print("Received Data:", response_data) 

            else:
                print("Empty response received from server.")

        except Exception as e:
            print("Error occurred during request:", e)
