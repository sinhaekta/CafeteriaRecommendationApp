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
                    cursor = connection.cursor()
                    cursor.execute("""
                        SELECT c.item_id, c.name AS item_name, c.comment, r.rating_value 
                        FROM Comment c 
                        LEFT JOIN Rating r ON c.item_id = r.item_id
                        -- Optionally join Item table if necessary
                        -- LEFT JOIN Item i ON c.item_id = i.item_id
                    """)
                    feedback = cursor.fetchall()
                    print("Number of feedback rows fetched:", len(feedback))

                    item_rating = {}

                    for item_id, item_name, comment, rating_value in feedback:
                        sentiment = TextBlob(comment).sentiment.polarity
                        rating_score = float(rating_value) if rating_value else 0.0

                        combined_score = sentiment + rating_score

                        if item_name in item_rating:
                            item_rating[item_name].append(combined_score)
                        else:
                            item_rating[item_name] = [combined_score]

                    print("Item Ratings:", item_rating)

                    average_score = {item_name: round(sum(scores) / len(scores), 2) for item_name, scores in item_rating.items()}

                    recommended_items = sorted(average_score.items(), key=lambda x: x[1], reverse=True)

                    recommended_items_list = [[item_name, score] for item_name, score in recommended_items]
                    recommended_items_json = json.dumps(recommended_items_list)
                    print(recommended_items_json)

                    return recommended_items_json

            except Exception as e:
                print("Error occurred:", e)
                return json.dumps({"error": str(e)})    
        
    @classmethod
    def roll_menu_item_query(cls, daily_menu):
            try:
                db = DBConnection()
                connection = db.get_connection()

                if connection:
                    cursor = connection.cursor()
                    
                    for item in daily_menu:
                        cursor.execute(
                            "INSERT INTO Daily_Menu (menu_date, item_id, item_name, item_category) VALUES (%s, %s, %s, %s)",
                            (item['menu_date'], item['item_id'], item['item_name'], item['item_category'])
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
                        "SELECT item_id, item_name, item_category FROM Daily_Menu WHERE menu_date = %s",
                        (today_date,)
                    )
                    items = cursor.fetchall()
                    cursor.close()

                    if items:
                        notification_message = f"Daily menu updated with the following items:\n"
                        for item in items:
                            notification_message += f"- {item[1]} ({item[2]})\n"
                        
                        cursor = connection.cursor()
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
    def delete_discard_item_query(cls, item_id):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()

                cursor.execute("UPDATE Menu_Item SET is_deleted = 1 WHERE item_id = %s", (item_id,))
                connection.commit()

                cursor.close()
                return json.dumps({"status": "success", "message": "Menu item soft deleted successfully"})
            else:
                return json.dumps({"status": "error", "message": "Failed to establish database connection"})

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
        finally:
            if connection:
                connection.close()
                
    @classmethod
    def send_feedback_notification_query(cls, item_id):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor(dictionary=True)
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
                    return json.dumps({"status": "error", "message": "Item not found"})

        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})
        finally:
            if connection:
                connection.close()