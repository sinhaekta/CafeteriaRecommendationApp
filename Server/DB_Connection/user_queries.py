import json
from DB_Connection.db_connect import DBConnection
from decimal import Decimal
from textblob import TextBlob
import traceback


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
    def add_menu_item(cls, name, price, description, category):
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
                #if cursor.rowcount > 0:
                return {"status": "success", "message": "Menu item deleted successfully."}
                #return {"status": "error", "message": "Menu item not found."}
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
    def view_menu_items(cls):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM Menu_Item")
                rows = cursor.fetchall()
                result = [
                    {
                        "item_id": row[0],
                        "name": row[1],
                        "price": float(row[2]) if isinstance(row[2], Decimal) else row[2],
                        "description": row[3],
                        "category": row[4],
                        "availability": row[5],
                        "likes": row[6],
                        "dislikes": row[7],
                        "recommend_rating": float(row[8]) if isinstance(row[8], Decimal) else row[8]
                    }
                    for row in rows
                ]
                cursor.close()
                return {"status": "success", "data": result}
            else:
                return {"status": "error", "message": "Failed to establish database connection."}
        
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            if connection:
                connection.close()

    #@classmethod
    @classmethod
    def view_recommended_menu(cls):
        try:
            db = DBConnection()
            connection = db.get_connection()

            if connection:
                cursor = connection.cursor()
                cursor.execute("SELECT item_id, comment FROM Comment")
                feedback = cursor.fetchall()
                print("Number of feedback rows fetched:", len(feedback))  

                item_rating = {}

                for feed in feedback:
                    item_id, comment = feed
                    sentiment = TextBlob(comment).sentiment.polarity
                    if item_id in item_rating:
                        item_rating[item_id].append(sentiment)
                    else:
                        item_rating[item_id] = [sentiment]

                print("Item Ratings:", item_rating)

                average_score = {item_id: round(sum(scores) / len(scores), 2) for item_id, scores in item_rating.items()}

                recommended_items = sorted(average_score.items(), key=lambda x: x[1], reverse=True)

                recommended_items_list = [[item_id, score] for item_id, score in recommended_items]
                recommended_items_json = json.dumps(recommended_items_list)
                print(recommended_items_json)  

                return recommended_items_json 

        except Exception as e:
            print("Error occurred:", e)
            return json.dumps({"error": str(e)}) 