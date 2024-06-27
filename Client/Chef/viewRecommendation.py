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
                if response.startswith('"') and response.endswith('"'):
                    response = response.strip('"')

                try:
                    response_data = json.loads(response)
                    print("Received Data:", response_data)
                    print("Type of Received Data:", type(response_data)) 

                    if isinstance(response_data, list):
                        for item in response_data:
                            print("Item:", item, "Type:", type(item))
                        
                        if all(isinstance(i, list) and len(i) == 2 for i in response_data):
                            headers = ["Item ID", "Average Sentiment Score"]
                            table = tabulate(response_data, headers, tablefmt="grid")
                            print(table)
                        else:
                            print("Data items are not in expected format (list of lists with two elements each).")
                    else:
                        print("Response data is not a list.")
                except json.JSONDecodeError as e:
                    print("JSON decoding failed:", e)
            else:
                print("Empty response received from server.")

        except Exception as e:
            print("Error occurred during request:", e)

