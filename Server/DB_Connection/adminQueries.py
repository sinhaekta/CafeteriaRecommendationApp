import json
from DB_Connection.dbConnect import DBConnection
from decimal import Decimal
import traceback

class AdminQuery:
    @classmethod
    def authenticate_user_query(cls, username):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT password, role, name FROM User WHERE name = %s", (username,))
                rows = cursor.fetchall()
                
                data = []
                for row in rows:
                    data.append({
                        "password": row[0],
                        "role": row[1]
                    })

                cursor.close()
                return data
            else:
                return json.dumps({})
            
        except Exception as e:
            print(f"Error fetching data: {e}")
            return json.dumps({})
        finally:
            if connection:
                connection.close()

    @classmethod
    def add_menu_item_query(cls, name, price, description, category):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute(
                    "INSERT INTO Menu_Item (name, price, description, category) VALUES (%s, %s, %s, %s)",
                    (name, price, description, category)
                )
                connection.commit()
                cursor.close()
                return {"status": "success", "message": "Menu item added successfully."}
            else:
                return {"status": "error", "message": "Failed to establish database connection."}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()

    @classmethod
    def delete_menu_item_query(cls, item_id):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM Menu_Item WHERE item_id = %s", (item_id,))
                connection.commit()
                cursor.close()
                return {"status": "success", "message": "Menu item deleted successfully."}
            else:
                return {"status": "error", "message": "Failed to establish database connection."}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()

    @classmethod
    def update_menu_item_query(cls, item_id, name, price, description, category):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute(
                    "UPDATE Menu_Item SET name = %s, price = %s, description = %s, category = %s WHERE item_id = %s",
                    (name, price, description, category, item_id)
                )
                connection.commit()
                
                if cursor.rowcount > 0:
                    return {"status": "success", "message": "Menu item updated successfully."}
                else:
                    return {"status": "error", "message": "Menu item not found."}
                cursor.close()
                return result            
            else:
                return {"status": "error", "message": "Failed to establish database connection."}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()
                
    @classmethod
    def view_menu_items_query(cls):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Menu_Item")
                rows = cursor.fetchall()
                cursor.close()
                connection.close()
                return rows 

            else:
                raise Exception("Failed to establish database connection.")

        except Exception as e:
            raise e   