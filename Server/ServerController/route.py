from Services.auth import Authentication
from Services.add_item import AddItem
from Services.roll_menu import RollMenu 
from DB_Connection.user_queries import UserQuery

class Route:
    @staticmethod
    def redirect_client_data(data):
        print("in route")
        print(data["path"])
        
        if data["path"] == "auth":
            response = Authentication.authenticate_user(data)
            return response
        
        elif data["path"] == "add_menu_item":
            response = AddItem.add_menu_item(data["name"], data["price"], data["description"], data["category"])
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
        
        elif data["path"] == "roll_menu_item":
            response = RollMenu.roll_menu(data["items"])
            return response
        
        elif data["path"] == "send_notification":
            response = UserQuery.send_notification()
            return response
        
        elif data["path"] == "check_notification":
            response = UserQuery.check_notification()
            return response
        
        elif data["path"] == "order_food":
            response = UserQuery.order_food(data)
            return response
        
        elif data["path"] == "fetch_employee_orders":
            response = UserQuery.fetch_employee_orders(data["user_id"])
            return response
        
        elif data["path"] == "give_feedback":
            response = UserQuery.give_feedback(data)
            return response

        else:
            return {"status": "error", "message": "Invalid path"}