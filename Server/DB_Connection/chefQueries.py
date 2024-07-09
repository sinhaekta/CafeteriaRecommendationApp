import json
from DB_Connection.dbConnect import DBConnection
from decimal import Decimal
from textblob import TextBlob
import traceback
from datetime import datetime
    
class ChefQuery:  
    @classmethod
    def view_recommended_menu_query(cls):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("""
                    SELECT c.item_id, c.name AS item_name, c.comment, r.rating_value 
                    FROM Comment c 
                    LEFT JOIN Rating r ON c.item_id = r.item_id
                """)
                feedback = cursor.fetchall()
                print("Number of feedback rows fetched:", len(feedback))

                cursor.close()
                connection.close()

                return feedback 

        except Exception as e:
            print("Error occurred:", e)
            return [] 
        
    @classmethod
    def update_avg_rating(cls, average_score):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                for item_name, score in average_score.items():
                    cursor.execute("""
                        UPDATE Menu_Item
                        SET avg_rating = %s
                        WHERE name = %s
                    """, (score, item_name))
                connection.commit()
                cursor.close()
                connection.close()

                return True  

        except Exception as e:
            print("Error occurred during avg_rating update:", e)
            return False
            
    @classmethod
    def roll_menu_item_query(cls, daily_menu):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()

                for item in daily_menu:
                    cursor.execute("""
                        SELECT AVG(avg_rating) AS average_rating
                        FROM Menu_Item
                        WHERE name = %s
                    """, (item['item_name'],))
                    result = cursor.fetchone()  

                    if result:
                        average_rating = result[0] if result[0] is not None else 0.0
                    else:
                        average_rating = 0.0  

                    cursor.execute(
                        "INSERT INTO Daily_Menu (menu_date, item_id, item_name, item_category, average_rating) VALUES (%s, %s, %s, %s, %s)",
                        (item['menu_date'], item['item_id'], item['item_name'], item['item_category'], average_rating)
                    )

                connection.commit()
                cursor.close()

                return {"status": "success", "message": "Daily menu updated successfully"}
            else:
                return {"status": "error", "message": "Failed to establish database connection"}

        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()
                  
    @classmethod
    def send_notification_query(cls):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                today_date = datetime.now().strftime("%Y-%m-%d")

                cursor.execute(
                    "SELECT * FROM Notification WHERE notification_date = %s",
                    (today_date,)
                )
                existing_notification = cursor.fetchone()

                if existing_notification:
                    return {"status": "error", "message": "Notification already sent for today."}

                cursor.execute(
                    "SELECT dm.item_id, dm.item_name, dm.item_category, mi.avg_rating "
                    "FROM Daily_Menu dm "
                    "LEFT JOIN Menu_Item mi ON dm.item_id = mi.item_id "
                    "WHERE dm.menu_date = %s",
                    (today_date,)
                )
                items = cursor.fetchall()

                if items:
                    notification_message = f"Menu for {today_date}:\n"
                    for item in items:
                        item_id = item[0]
                        item_name = item[1]
                        item_category = item[2]
                        avg_rating = item[3] if item[3] is not None else "N/A"
                        notification_message += f"- Item ID: {item_id}, {item_name} ({item_category}) - Rating: {avg_rating}\n"

                    cursor.execute(
                        "INSERT INTO Notification (message, notification_date) VALUES (%s, %s)",
                        (notification_message, today_date)
                    )
                    connection.commit()
                    cursor.close()

                    return {"status": "success", "message": "Notification sent successfully."}
                else:
                    return {"status": "error", "message": "No items found in the daily menu for today."}

            else:
                return {"status": "error", "message": "Failed to establish database connection."}

        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()
                    
    @classmethod
    def view_discard_menu_query(cls):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor(dictionary=True)
                cursor.execute("""
                    SELECT r.item_id, m.name as item_name, MIN(r.rating_value) as rating_value
                    FROM Rating r
                    JOIN Menu_Item m ON r.item_id = m.item_id
                    WHERE m.is_deleted = 0  
                    GROUP BY r.item_id, m.name
                    ORDER BY rating_value ASC
                    LIMIT 2
                """)
                items_to_discard = cursor.fetchall()
                print("Items to discard:", items_to_discard)

                cursor.execute("DELETE FROM Discard_Items")

                for item in items_to_discard:
                    cursor.execute("""
                        INSERT INTO Discard_Items (item_id, item_name, rating_value)
                        VALUES (%s, %s, %s)
                    """, (item['item_id'], item['item_name'], item['rating_value']))

                connection.commit()

                cursor.execute("SELECT * FROM Discard_Items")
                discard_menu = cursor.fetchall()
                print("Discard menu items:", discard_menu)

                cursor.close()
                connection.close()

                return json.dumps(discard_menu)
            else:
                print("Failed to establish database connection.")
                return json.dumps({"status": "error", "message": "Failed to establish database connection."})

        except Exception as e:
            print("Error occurred:", e)
            return json.dumps({"error": str(e)})
                
    @classmethod
    def send_feedback_notification_query(cls, item_id):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor(dictionary=True)
                

                today_date = datetime.now().strftime("%Y-%m-%d")
                cursor.execute(
                    "SELECT * FROM Discard_Item_Notification WHERE item_id = %s AND DATE(notification_date) = %s",
                    (item_id, today_date)
                )
                existing_notification = cursor.fetchone()

                if existing_notification:
                    cursor.close()
                    return json.dumps({"status": "error", "message": "Duplicate entry for Notification!"})
                
                cursor.execute("SELECT name FROM Menu_Item WHERE item_id = %s", (item_id,))
                item = cursor.fetchone()

                if item:
                    item_name = item['name']
                    message = (
                        f"We are trying to improve your experience with {item_name}. "
                        "Please provide your feedback and help us. "
                        f"Q1. What didn’t you like about {item_name}?\n"
                        f"Q2. How would you like {item_name} to taste?\n"
                        f"Q3. Share your mom’s recipe."
                    )
                    notification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    cursor.execute("""
                        INSERT INTO Discard_Item_Notification (item_id, message, notification_date)
                        VALUES (%s, %s, %s)
                    """, (item_id, message, notification_date))

                    connection.commit()
                    cursor.close()
                    return json.dumps({"status": "success", "message": "Notification sent successfully"})
                else:
                    cursor.close()
                    return json.dumps({"status": "error", "message": "Item not found"})

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
        finally:
            if connection:
                connection.close()
                
    @classmethod
    def delete_discard_item_query(cls, item_id):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()

                cursor.execute("UPDATE Menu_Item SET is_deleted = 1 WHERE item_id = %s", (item_id,))
                connection.commit()

                cursor.execute("UPDATE Discard_Items SET is_deleted = 1 WHERE item_id = %s", (item_id,))
                connection.commit()

                cursor.close()
                return json.dumps({"status": "success", "message": "Item Deleted successfully"})
            else:
                return json.dumps({"status": "error", "message": "Failed to establish database connection"})

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
        finally:
            if connection:
                connection.close()

