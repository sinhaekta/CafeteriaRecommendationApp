from DB_Connection.chefQueries import ChefQuery
from datetime import datetime
import json

class ChefServiceHandler:
    @staticmethod
    def view_recommended_menu():
        try:
            recommended_items_json = ChefQuery.view_recommended_menu_query()
            return recommended_items_json
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def roll_menu(items):
        try:
            daily_menu = [
                {
                    "menu_date": datetime.now().strftime("%Y-%m-%d"),
                    "item_id": item['item_id'],
                    "item_name": item['item_name'],
                    "item_category": item['item_category']
                }
                for item in items
            ]
            return ChefQuery.roll_menu_item_query(daily_menu)
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def send_notification():
        try:
            return ChefQuery.send_notification_query()
        except Exception as e:
            return {"status": "error", "message": str(e)}
             
    @staticmethod
    def view_discard_menu():
        try:
            discard_menu_json = ChefQuery.view_discard_menu_query()
            print("Discard menu JSON:", discard_menu_json)
            return discard_menu_json
        except Exception as e:
            return json.dumps({"status": "error", "message": str(e)})