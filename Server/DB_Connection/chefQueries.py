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
                    
        
        