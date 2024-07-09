from DB_Connection.chefQueries import ChefQuery
from datetime import datetime
from textblob import TextBlob
import json

class ChefServiceHandler:
    @staticmethod
    def view_recommended_menu():
        try:
            feedback_data = ChefQuery.view_recommended_menu_query()

            if not feedback_data:
                return json.dumps({"status": "error", "message": "No feedback data available"})

            item_rating = {}

            for row in feedback_data:
                item_id = row['item_id']
                item_name = row['item_name']
                comment = row['comment']
                rating_value = row['rating_value']

                sentiment = TextBlob(comment).sentiment.polarity
                rating_score = float(rating_value) if rating_value else 0.0

                combined_score = sentiment + rating_score

                if item_name in item_rating:
                    item_rating[item_name].append(combined_score)
                else:
                    item_rating[item_name] = [combined_score]

            print("Item Ratings:", item_rating)

            average_score = {item_name: round(min(sum(scores) / len(scores), 5.0), 2) for item_name, scores in item_rating.items()}

            update_status = ChefQuery.update_avg_rating(average_score)

            if not update_status:
                return json.dumps({"status": "error", "message": "Failed to update average ratings in Menu_Item table"})

            recommended_items = sorted(average_score.items(), key=lambda x: x[1], reverse=True)
            recommended_items_list = [{"item_name": item_name, "average_score": score} for item_name, score in recommended_items]
            recommended_items_json = json.dumps(recommended_items_list)
            print(recommended_items_json)

            return recommended_items_json

        except Exception as e:
            error_message = f"Error occurred in view_recommended_menu: {str(e)}"
            print(error_message)
            return json.dumps({"status": "error", "message": error_message})

    @staticmethod
    def roll_menu(items):
        try:
            if not items:
                return json.dumps({"status": "error", "message": "No items provided for rolling menu"})

            daily_menu = [
                {
                    "menu_date": datetime.now().strftime("%Y-%m-%d"),
                    "item_id": item['item_id'],
                    "item_name": item['item_name'],
                    "item_category": item['item_category']
                }
                for item in items
            ]

            result = ChefQuery.roll_menu_item_query(daily_menu)
            return json.dumps(result)

        except Exception as e:
            error_message = f"Error occurred in roll_menu: {str(e)}"
            print(error_message)
            return json.dumps({"status": "error", "message": error_message})

    @staticmethod
    def send_notification():
        try:
            return ChefQuery.send_notification_query()
        
        except Exception as e:
            error_message = f"Error occurred in send_notification: {str(e)}"
            print(error_message)
            return json.dumps({"status": "error", "message": error_message})
             
    @staticmethod
    def view_discard_menu():
        try:
            discard_menu_json = ChefQuery.view_discard_menu_query()

            if not discard_menu_json:
                return json.dumps({"status": "error", "message": "No discard menu data available"})

            print("Discard menu JSON:", discard_menu_json)
            return discard_menu_json
        
        except Exception as e:
            error_message = f"Error occurred in view_discard_menu: {str(e)}"
            print(error_message)
            return json.dumps({"status": "error", "message": error_message})

    @staticmethod
    def delete_discard_item(item_id):
        try:
            return ChefQuery.delete_discard_item_query(item_id)
        
        except Exception as e:
            error_message = f"Error occurred in delete_discard_item: {str(e)}"
            return json.dumps({"status": "error", "message": error_message})

    @staticmethod
    def send_feedback_notification(item_id):
        try:
            return ChefQuery.send_feedback_notification_query(item_id)
        
        except Exception as e:
            error_message = f"Error occurred in send_feedback_notification: {str(e)}"
            return json.dumps({"status": "error", "message": error_message})