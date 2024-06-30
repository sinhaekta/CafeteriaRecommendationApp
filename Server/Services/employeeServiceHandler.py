from DB_Connection.employeeQueries import EmployeeQuery
from datetime import datetime, date

class EmployeeServiceHandler:
    
    @staticmethod
    def check_notification():
        try:
            notifications_data = EmployeeQuery.check_notification_query()
            return notifications_data
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def order_food(data):
        try:
            order_result = EmployeeQuery.order_food_query(data)
            return order_result
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def fetch_employee_orders(user_id):
        try:
            orders_data = EmployeeQuery.fetch_employee_orders_query(user_id)
            return orders_data
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def give_feedback(data):
        try:
            feedback_result = EmployeeQuery.give_feedback_query(data)
            return feedback_result
        except Exception as e:
            return {"status": "error", "message": str(e)}
        
    @staticmethod
    def give_feedback_discard_item(data):
        try:
            feedback_result = EmployeeQuery.give_feedback_discard_item_query(data)
            return feedback_result
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def fetch_discard_item_notifications():
        try:
            notifications_data = EmployeeQuery.fetch_discard_item_notifications_query()
            return notifications_data
        except Exception as e:
            return {"status": "error", "message": str(e)}