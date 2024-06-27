from DB_Connection.user_queries import UserQuery
from datetime import datetime

class RollMenu:
    @staticmethod
    def roll_menu(items):
        daily_menu = [
            {
                "menu_date": datetime.now().strftime("%Y-%m-%d"),
                "item_id": item['item_id'],
                "item_name": item['item_name'],
                "item_category": item['item_category']
            }
            for item in items
        ]
        return UserQuery.roll_menu_item(daily_menu)
