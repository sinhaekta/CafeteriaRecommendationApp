from DB_Connection.user_queries import UserQuery

class AddItem:
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
            
            feedback = UserQuery.add_menu_item_query(name, price, description, category)
            return feedback

        except ValueError as ve:
            print("Input validation error:", ve)
            return {"status": "error", "message": str(ve)}

        except Exception as e:
            print("Error occurred:", e)
            return {"status": "error", "message": str(e)}

