import json
from tabulate import tabulate
from client import client_connection  

class DiscardMenu:
    def __init__(self):
        pass
    
    def view_discard_menu(self):
        try:
            request_data = {
                "path": "view_discard_menu"
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
                        headers = ["Discard ID", "Item ID", "Item Name", "Rating Value"]
                        table_data = [[item["discard_id"], item["item_id"], item["item_name"], item["rating_value"]] for item in response_data]
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