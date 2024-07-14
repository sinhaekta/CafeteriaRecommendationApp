from DB_Connection.AdminDBOperations import AdminDBOperation
from DB_Connection.AdminDBOperations import AdminDBOperation
from decimal import Decimal
import pymysql

class AdminService:
    @staticmethod
    def add_menu_item(name, price, description, category):
        try:
            MIN_PRICE_THRESHOLD = 0  
            
            if not name:
                raise ValueError("Item name cannot be empty.")
            if not isinstance(price, (int, float)) or price <= MIN_PRICE_THRESHOLD:
                raise ValueError("Price must be a positive number.")
            if not description:
                raise ValueError("Description cannot be empty.")
            if not category:
                raise ValueError("Category cannot be empty.")
            
            feedback = AdminDBOperation.add_menu_item_query(name, price, description, category)
            return feedback

        except ValueError as ve:
            print("Input validation error:", ve)
            return {"status": "error", "message": str(ve)}

        except Exception as e:
            print("Error occurred:", e)
            return {"status": "error", "message": str(e)}
        
    @staticmethod
    def delete_menu_item(item_id):
        try:
            if not isinstance(item_id, int) or item_id <= 0:
                raise ValueError("Invalid item_id. It must be a positive integer.")

            response = AdminDBOperation.delete_menu_item_query(item_id)
            
            if response.get("status") == "success":
                return {"status": "success", "message": "Menu item deleted successfully."}
            else:
                return {"status": "error", "message": response.get("message", "Unknown error")}
        
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}
        
        except Exception as e:
            return {"status": "error", "message": f"Failed to delete item with ID {item_id}: {str(e)}"}
           
    @staticmethod
    def update_menu_item(item_id, name, price, description, category):
        try:

            if not isinstance(item_id, int) or item_id <= 0:
                raise ValueError("Invalid item_id. It must be a positive integer.")
            
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Invalid name. It must be a non-empty string.")
            
            if not isinstance(price, (int, float)) or price <= 0:
                raise ValueError("Invalid price. It must be a positive number.")
            
            if not isinstance(description, str) or not description.strip():
                raise ValueError("Invalid description. It must be a non-empty string.")
            
            if not isinstance(category, str) or not category.strip():
                raise ValueError("Invalid category. It must be a non-empty string.")

            response = AdminDBOperation.update_menu_item_query(item_id, name, price, description, category)

            if response.get("status") == "success":
                return {"status": "success", "message": "Menu item updated successfully."}
            else:
                return {"status": "error", "message": response.get("message", "Unknown error")}
        
        except ValueError as ve:
            return {"status": "error", "message": str(ve)}
        
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}

    @staticmethod
    def view_menu_items():
        try:
            rows = AdminDBOperation.view_menu_items_query()

            result = [
                {
                    "item_id": row[0],
                    "name": row[1],
                    "price": float(row[2]) if isinstance(row[2], Decimal) else row[2],
                    "description": row[3],
                    "category": row[4],
                }
                for row in rows
            ]

            return {"status": "success", "data": result}

        except ValueError as ve:
            return {"status": "error", "message": str(ve)}

        except pymysql.Error as my_sql_err:
            return {"status": "error", "message": f"MySQL error: {str(my_sql_err)}"}

        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}