from Services.AuthenticationService import AuthenticationService
from Services.AdminService import AdminService
from Services.ChefService import ChefService
from Services.EmployeeService import EmployeeService

class RouteController:
    @staticmethod
    def redirect_client_data(data):
        print(data["path"])
        
        if data["path"] == "auth":
            response = AuthenticationService.authenticate_user(data)
            return response
        
        elif data["path"] == "add_menu_item":
            response = AdminService.add_menu_item(data["name"], data["price"], data["description"], data["category"])
            return response

        elif data["path"] == "delete_menu_item":
            response = AdminService.delete_menu_item(data["item_id"])
            return response

        elif data["path"] == "update_menu_item":
            response = AdminService.update_menu_item(data["item_id"], data["name"], data["price"], data["description"], data["category"])
            return response

        elif data["path"] == "view_menu_items":
            response = AdminService.view_menu_items()
            return response
 
        elif data["path"] == "view_recommended_menu":
            response = ChefService.view_recommended_menu()  
            return response       
        
        elif data["path"] == "roll_menu_item":
            response = ChefService.roll_menu(data["items"])
            return response
        
        elif data["path"] == "send_notification":
            response = ChefService.send_notification()
            return response
        
        elif data["path"] == "check_notification":
            response = EmployeeService.check_notification()
            return response
        
        elif data["path"] == "order_food":
            response = EmployeeService.order_food(data)
            return response
        
        elif data["path"] == "fetch_employee_orders":
            response = EmployeeService.fetch_employee_orders(data["user_id"])
            return response
        
        elif data["path"] == "give_feedback":
            response = EmployeeService.give_feedback(data)
            return response
        
        elif data["path"] == "view_discard_menu":
            response = ChefService.view_discard_menu()
            return response
        
        elif data["path"] == "delete_discard_item":
            response = ChefService.delete_discard_item(data["item_id"])
            return response
        
        elif data["path"] == "send_feedback_notification":
            response = ChefService.send_feedback_notification(data["item_id"])
            return response
        
        elif data["path"] == "fetch_discard_item_notifications":
            response = EmployeeService.fetch_discard_item_notifications()
            return response
        
        elif data["path"] == "give_feedback_discard_item":
            response = EmployeeService.give_feedback_discard_item(data)
            return response
        
        elif data["path"] == "update_profile":
            response = EmployeeService.update_user_profile(data)
            return response

        else:
            return {"status": "error", "message": "Invalid path"}
