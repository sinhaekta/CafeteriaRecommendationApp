import json
from tabulate import tabulate
from Client import client_connection

class DiscardMenu:
    def __init__(self):
        pass
    
    def view_discard_menu(self):
        try:
            request_data = {
                "path": "view_discard_menu"
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
                        headers = ["Discard ID", "Item ID", "Item Name", "Rating Value"]
                        table_data = [[item.get("discard_id", ""),
                                       item.get("item_id", ""),
                                       item.get("item_name", ""),
                                       item.get("rating_value", "")] for item in response_data]
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
