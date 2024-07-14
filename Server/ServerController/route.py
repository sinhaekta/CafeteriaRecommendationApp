from Services.auth import Authentication
from Services.adminServiceHandler import AdminServiceHandler
from Services.chefServiceHandler import ChefServiceHandler
from Services.employeeServiceHandler import EmployeeServiceHandler

class Route:
    @staticmethod
    def redirect_client_data(data):
        print("in route")
        print(data["path"])
        
        if data["path"] == "auth":
            response = Authentication.authenticate_user(data)
            return response
        
        elif data["path"] == "add_menu_item":
            response = AdminServiceHandler.add_menu_item(data["name"], data["price"], data["description"], data["category"])
            return response

        elif data["path"] == "delete_menu_item":
            response = AdminServiceHandler.delete_menu_item(data["item_id"])
            return response

        elif data["path"] == "update_menu_item":
            response = AdminServiceHandler.update_menu_item(data["item_id"], data["name"], data["price"], data["description"], data["category"])
            return response

        elif data["path"] == "view_menu_items":
            response = AdminServiceHandler.view_menu_items()
            return response
 
        elif data["path"] == "view_recommended_menu":
            response = ChefServiceHandler.view_recommended_menu()  
            return response       
        
        elif data["path"] == "roll_menu_item":
            response = ChefServiceHandler.roll_menu(data["items"])
            return response
        
        elif data["path"] == "send_notification":
            response = ChefServiceHandler.send_notification()
            return response
        
        elif data["path"] == "check_notification":
            response = EmployeeServiceHandler.check_notification()
            return response
        
        elif data["path"] == "order_food":
            response = EmployeeServiceHandler.order_food(data)
            return response
        
        elif data["path"] == "fetch_employee_orders":
            response = EmployeeServiceHandler.fetch_employee_orders(data["user_id"])
            return response
        
        elif data["path"] == "give_feedback":
            response = EmployeeServiceHandler.give_feedback(data)
            return response
        
        elif data["path"] == "view_discard_menu":
            response = ChefServiceHandler.view_discard_menu()
            return response
        
        elif data["path"] == "delete_discard_item":
            response = ChefServiceHandler.delete_discard_item(data["item_id"])
            return response
        
        elif data["path"] == "send_feedback_notification":
            response = ChefServiceHandler.send_feedback_notification(data["item_id"])
            return response
        
        elif data["path"] == "fetch_discard_item_notifications":
            response = EmployeeServiceHandler.fetch_discard_item_notifications()
            return response
        
        elif data["path"] == "give_feedback_discard_item":
            response = EmployeeServiceHandler.give_feedback_discard_item(data)
            return response
        
        elif data["path"] == "update_profile":
            response = EmployeeServiceHandler.update_user_profile(data)
            return response

        else:
            return {"status": "error", "message": "Invalid path"}
