import json
from tabulate import tabulate
from client import client_connection  

class Recommendation:
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
                try:
                    response = response.replace('\\"', '"')
                    
                    if response.startswith('"') and response.endswith('"'):
                        response = response.strip('"')
                    response_data = json.loads(response)
                    
                    print("Received Data:", response_data)
                    print("Type of Received Data:", type(response_data)) 

                    if isinstance(response_data, list):
                        headers = ["Item Name", "Average Score"]
                        table_data = [[item[0], item[1]] for item in response_data]
                        table = tabulate(table_data, headers, tablefmt="grid")
                        print(table)
                    else:
                        print("Response data is not in expected format (list).")

                except json.JSONDecodeError as e:
                    print("JSON decoding failed:", e)
                    print("Invalid format in response:", response)
            
            else:
                print("Empty response received from server.")

        except Exception as e:
            print("Error occurred during request:", e)