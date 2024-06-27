import json
from client import client_connection
from tabulate import tabulate

class ViewMenu:
    def __init__(self):
        pass
    
    def view_menu_items(self):
        request_data = {
            "path": "view_menu_items"
        }

        request_json = json.dumps(request_data)
        response = client_connection(request_json)
        
        response = json.loads(response)
        
        if response["status"] == "success":
            data = response["data"]
            headers = ["Item ID", "Name", "Price", "Description", "Category", "Availability", "Likes", "Dislikes", "Recommend Rating"]
            table = [[item["item_id"], item["name"], item["price"], item["description"], item["category"], item["availability"], item["likes"], item["dislikes"], item["recommend_rating"]] for item in data]
            print(tabulate(table, headers, tablefmt="grid"))
        else:
            print(response["message"])



