import json
from DB_Connection.dbConnect import DBConnection
from decimal import Decimal
from textblob import TextBlob
import traceback
from datetime import datetime
from datetime import date

class EmployeeQuery:  
    @classmethod
    def check_notification_query(cls):
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
    def order_food_query(cls, data):
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
    def fetch_employee_orders_query(cls, user_id):
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
    def give_feedback_query(cls, data):
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
             
    @classmethod
    def give_feedback_discard_item_query(cls, data):
        try:
            user_id = data['user_id']
            notification_id = data['notification_id']
            feedback = data['feedback']
            feedback_date = datetime.now().strftime("%Y-%m-%d")

            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()

                cursor.execute("""
                    INSERT INTO Employee_Discard_Item_Feedback (user_id, notification_id, feedback, feedback_date)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, notification_id, feedback, feedback_date))

                connection.commit()
                cursor.close()

                return {"status": "success", "message": "Feedback submitted successfully"}
            else:
                return {"status": "error", "message": "Failed to establish database connection"}

        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()
                
    @classmethod
    def fetch_discard_item_notifications_query(cls):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Discard_Item_Notification ORDER BY notification_date DESC")
                notifications = cursor.fetchall()
                cursor.close()

                if notifications:
                    formatted_notifications = [
                        {
                            "notification_id": notification[0],
                            "item_id": notification[1],
                            "message": notification[2],
                            "notification_date": notification[3].strftime("%Y-%m-%d")
                        }
                        for notification in notifications
                    ]
                    return {"status": "success", "data": formatted_notifications}
                else:
                    return {"status": "error", "message": "No discard item notifications found."}
            else:
                return {"status": "error", "message": "Failed to establish database connection."}

        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()
                
    @classmethod
    def update_user_profile_query(cls, profile_data):
        try:
            user_id = profile_data['user_id']
            diet_type = profile_data['diet_type']
            spice_level = profile_data['spice_level']
            cuisine_preference = profile_data['cuisine_preference']
            sweet_tooth = profile_data['sweet_tooth']

            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM User WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()

                if not user:
                    return {"status": "error", "message": "User not found."}

                cursor.execute("SELECT * FROM Employee_Profile WHERE user_id = %s", (user_id,))
                existing_profile = cursor.fetchone()

                if existing_profile:
                    cursor.execute("""
                        UPDATE Employee_Profile 
                        SET diet_type = %s, spice_level = %s, cuisine_preference = %s, sweet_tooth = %s
                        WHERE user_id = %s
                    """, (diet_type, spice_level, cuisine_preference, sweet_tooth, user_id))
                else:
                    cursor.execute("""
                        INSERT INTO Employee_Profile (user_id, diet_type, spice_level, cuisine_preference, sweet_tooth)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (user_id, diet_type, spice_level, cuisine_preference, sweet_tooth))

                connection.commit()
                cursor.close()
                return {"status": "success", "message": "User profile updated successfully."}

            else:
                return {"status": "error", "message": "Failed to establish database connection."}

        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()
