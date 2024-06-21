import json
from client import client_connection

class viewMenu:
    def __init__(self):
        pass
    
    def view_menu_items(self):
        request_data = {
            "path": "view_menu_items"
        }

        request_json = json.dumps(request_data)
        response = client_connection(request_json)
        print(response)
