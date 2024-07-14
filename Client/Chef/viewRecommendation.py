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
            response = client_connection(request_json)

            if response:
                try:
                    response = response.replace('\\"', '"')

                    if response.startswith('"') and response.endswith('"'):
                        response = response.strip('"')

                    response_data = json.loads(response)

                    if isinstance(response_data, list):
                        headers = ["Item Name", "Average Score"]
                        table_data = [[item.get("item_name", ""),
                                       item.get("average_score", "")] for item in response_data]
                        table = tabulate(table_data, headers, tablefmt="grid")
                        print(table)
                    else:
                        print("Response data is not in expected format (list).")

                except json.JSONDecodeError as e:
                    print("JSON decoding failed:", e)
                    print("Invalid format in response:", response)
            
            else:
                print("Empty response received from server.")

        except ConnectionError:
            print("Failed to connect to the server. Please check your network connection and try again.")
        except Exception as e:
            print("Error occurred during request:", e)