from auth import Authentication
from DB_Connection.user_queries import UserQuery

class Route:
    @staticmethod
    def redirect(data):
        print("in route")
        print(data["path"])
        
        if data["path"] == "auth":
            response = Authentication.authenticateUser(data)
            return response
        
        elif data["path"] == "add_menu_item":
            response = UserQuery.add_menu_item(data["name"], data["price"], data["description"], data["category"])
            return response

        elif data["path"] == "delete_menu_item":
            response = UserQuery.delete_menu_item(data["item_id"])
            return response

        elif data["path"] == "update_menu_item":
            response = UserQuery.update_menu_item(data["item_id"], data["name"], data["price"], data["description"], data["category"])
            return response

        elif data["path"] == "view_menu_items":
            response = UserQuery.view_menu_items()
            return response
 
        elif data["path"] == "view_recommended_menu":
            response = UserQuery.view_recommended_menu()
            return response       
        

        return {"status": "error", "message": "Invalid path"}
