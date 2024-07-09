import unittest
from unittest.mock import patch
import json
from textblob import TextBlob
from DB_Connection.chefQueries import ChefQuery
from Services.chefServiceHandler import ChefServiceHandler

class TestChefServiceHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('testValues.json') as f:
            cls.test_values = json.load(f)
            
    @patch.object(ChefQuery, 'view_recommended_menu_query')
    @patch.object(ChefQuery, 'update_avg_rating')
    @patch('textblob.TextBlob') 
    def test_view_recommended_menu(self, mock_textblob, mock_update_avg_rating, mock_view_recommended_menu_query):
        mock_textblob.return_value.sentiment.polarity = self.test_values['valid_sentiment_polarity'] 
        mock_textblob.return_value.sentiment.subjectivity = self.test_values['valid_sentiment_subjectivity'] 

        mock_view_recommended_menu_query.return_value = self.test_values['recommended_menu_items']

        mock_update_avg_rating.return_value = True

        expected_output = [
            {"item_name": "Dish1", "average_score": self.test_values['valid_expected_average']}, 
            {"item_name": "Dish2", "average_score": self.test_values['valid_expected_average']}   
        ]
        expected_json = json.dumps(expected_output)

        result = ChefServiceHandler.view_recommended_menu()
        result_obj = json.loads(result) 

        self.assertEqual(len(result_obj), len(expected_output))  

        for expected_item, result_item in zip(expected_output, result_obj):
            self.assertEqual(result_item['item_name'], expected_item['item_name'])  
            self.assertEqual(result_item['average_score'], expected_item['average_score'])

    @patch.object(ChefQuery, 'roll_menu_item_query')
    def test_roll_menu(self, mock_roll_menu_item_query):
        items = [{'item_id': self.test_values["valid_item_id"], 'item_name': self.test_values["valid_name"], 'item_category': self.test_values["valid_category"]}]
        mock_roll_menu_item_query.return_value = {"status": "success", "message": "Menu rolled successfully"}

        result = ChefServiceHandler.roll_menu(items)
        expected_result = json.dumps({"status": "success", "message": "Menu rolled successfully"})

        self.assertEqual(result, expected_result)

    @patch.object(ChefQuery, 'send_notification_query')
    def test_send_notification(self, mock_send_notification_query):
        mock_send_notification_query.return_value = {"status": "success", "message": "Notification sent successfully"}

        result = ChefServiceHandler.send_notification()
        expected_result = {"status": "success", "message": "Notification sent successfully"}

        self.assertEqual(result, expected_result)

    @patch.object(ChefQuery, 'view_discard_menu_query')
    def test_view_discard_menu(self, mock_view_discard_menu_query):
        mock_view_discard_menu_query.return_value = [
            {"discard_id": self.test_values["valid_discard_id"], "item_id": self.test_values["valid_item_id"], "item_name": self.test_values["valid_name"], "rating_value": self.test_values["valid_rating"]}
        ]

        expected_output = [
            {"discard_id": self.test_values["valid_discard_id"], "item_id": self.test_values["valid_item_id"], "item_name": self.test_values["valid_name"], "rating_value": self.test_values["valid_rating"]}
        ]
        expected_json = json.dumps(expected_output)

        result = ChefServiceHandler.view_discard_menu()
        result_json = json.dumps(result)

        self.assertEqual(result_json, expected_json)

    @patch.object(ChefQuery, 'delete_discard_item_query')
    def test_delete_discard_item(self, mock_delete_discard_item_query):
        item_id = self.test_values["valid_item_id"]
        mock_delete_discard_item_query.return_value = {"status": "success", "message": "Item deleted successfully"}

        result = ChefServiceHandler.delete_discard_item(item_id)
        expected_result = {"status": "success", "message": "Item deleted successfully"}

        self.assertEqual(result, expected_result)

    @patch.object(ChefQuery, 'send_feedback_notification_query')
    def test_send_feedback_notification(self, mock_send_feedback_notification_query):
        item_id = self.test_values["valid_item_id"]
        mock_send_feedback_notification_query.return_value = {"status": "success", "message": "Feedback notification sent successfully"}

        result = ChefServiceHandler.send_feedback_notification(item_id)
        expected_result = {"status": "success", "message": "Feedback notification sent successfully"}

        self.assertEqual(result, expected_result)