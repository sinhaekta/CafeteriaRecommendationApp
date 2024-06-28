import json
from DB_Connection.db_connect import DBConnection
from decimal import Decimal
from textblob import TextBlob
import traceback
from datetime import datetime
from datetime import date


class UserQuery:
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
    def delete_menu_item(cls, item_id):
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
    def update_menu_item(cls, item_id, name, price, description, category):
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
    def view_recommended_menu(cls):
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
    def roll_menu_item(cls, daily_menu):
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
    def send_notification(cls):
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
    def check_notification(cls):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Notification ORDER BY notification_date DESC")
                notifications = cursor.fetchall()
                cursor.close()

                if notifications:
                    formatted_notifications = [
                        {
                            "notification_id": notification[0],
                            "message": notification[1],
                            "notification_date": notification[2].strftime("%Y-%m-%d")
                        }
                        for notification in notifications
                    ]
                    return {"status": "success", "data": formatted_notifications}
                else:
                    return {"status": "error", "message": "No notifications found."}
            else:
                return {"status": "error", "message": "Failed to establish database connection."}

        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()
                
    @classmethod
    def order_food(cls, data):
        try:
            user_id = data['user_id']
            breakfast_item_id = data['breakfast_item_id']
            lunch_item_id = data['lunch_item_id']
            dinner_item_id = data['dinner_item_id']
            order_date = date.today()

            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()

                cursor.execute(
                    """
                    INSERT INTO Employee_Orders (user_id, breakfast_item_id, lunch_item_id, dinner_item_id, order_date) 
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (user_id, breakfast_item_id, lunch_item_id, dinner_item_id, order_date)
                )

                connection.commit()
                cursor.close()

                return {"status": "success", "message": "Vote submitted successfully"}
            else:
                return {"status": "error", "message": "Failed to establish database connection"}

        except Exception as e:
            print(f"Error occurred: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()
                
    @classmethod
    def fetch_employee_orders(cls, user_id):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT eo.order_id, eo.breakfast_item_id, eo.lunch_item_id, eo.dinner_item_id,
                        mi1.name AS breakfast_item_name, mi2.name AS lunch_item_name, mi3.name AS dinner_item_name
                    FROM Employee_Orders eo
                    LEFT JOIN Menu_Item mi1 ON eo.breakfast_item_id = mi1.item_id
                    LEFT JOIN Menu_Item mi2 ON eo.lunch_item_id = mi2.item_id
                    LEFT JOIN Menu_Item mi3 ON eo.dinner_item_id = mi3.item_id
                    WHERE eo.user_id = %s
                """, (user_id,))
                orders = cursor.fetchall()
                cursor.close()

                if orders:
                    formatted_orders = [
                        {
                            "order_id": order[0],
                            "breakfast_item_id": order[1],
                            "lunch_item_id": order[2],
                            "dinner_item_id": order[3],
                            "breakfast_item_name": order[4] if order[1] else "Not available",
                            "lunch_item_name": order[5] if order[2] else "Not available",
                            "dinner_item_name": order[6] if order[3] else "Not available"
                        }
                        for order in orders
                    ]
                    return {"status": "success", "data": formatted_orders}
                else:
                    return {"status": "error", "message": "No orders found for this user."}
            else:
                return {"status": "error", "message": "Failed to establish database connection."}

        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()


    @classmethod
    def give_feedback(cls, data):
        try:
            order_id = data['order_id']
            feedback_list = data.get('feedback', [])  

            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()

                for feedback in feedback_list:
                    item_id = feedback.get('item_id')
                    rating = feedback.get('rating')
                    comment = feedback.get('comment')

                    if rating is not None:
                        cursor.execute("""
                            INSERT INTO Rating (item_id, rating_value)
                            SELECT %s, %s
                            FROM Employee_Orders
                            WHERE order_id = %s
                        """, (item_id, rating, order_id))

                    if comment:
                        cursor.execute("""
                            INSERT INTO Comment (user_id, item_id, name, comment, comment_date)
                            SELECT eo.user_id, eo.breakfast_item_id, mi.name, %s, CURDATE()
                            FROM Employee_Orders eo
                            JOIN Menu_Item mi ON eo.breakfast_item_id = mi.item_id
                            WHERE eo.order_id = %s AND eo.breakfast_item_id = %s
                        """, (comment, order_id, item_id))
                        cursor.execute("""
                            INSERT INTO Comment (user_id, item_id, name, comment, comment_date)
                            SELECT eo.user_id, eo.lunch_item_id, mi.name, %s, CURDATE()
                            FROM Employee_Orders eo
                            JOIN Menu_Item mi ON eo.lunch_item_id = mi.item_id
                            WHERE eo.order_id = %s AND eo.lunch_item_id = %s
                        """, (comment, order_id, item_id))
                        cursor.execute("""
                            INSERT INTO Comment (user_id, item_id, name, comment, comment_date)
                            SELECT eo.user_id, eo.dinner_item_id, mi.name, %s, CURDATE()
                            FROM Employee_Orders eo
                            JOIN Menu_Item mi ON eo.dinner_item_id = mi.item_id
                            WHERE eo.order_id = %s AND eo.dinner_item_id = %s
                        """, (comment, order_id, item_id))

                connection.commit()
                cursor.close()

                return {"status": "success", "message": "Feedback submitted successfully"}
            else:
                return {"status": "error", "message": "Failed to establish database connection."}

        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()