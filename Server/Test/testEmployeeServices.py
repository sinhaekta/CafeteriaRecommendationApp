import unittest
from unittest.mock import patch
import json
from DB_Connection.employeeQueries import EmployeeQuery
from Services.employeeServiceHandler import EmployeeServiceHandler

class TestEmployeeServiceHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('testValues.json') as f:
            cls.test_values = json.load(f)

    @patch.object(EmployeeQuery, 'check_notification_query')
    def test_check_notification(self, mock_check_notification_query):
        mock_check_notification_query.return_value = self.test_values['valid_notifications']

        result = EmployeeServiceHandler.check_notification()
        expected_result = self.test_values['valid_notifications']

        self.assertEqual(result, expected_result)

    @patch.object(EmployeeQuery, 'order_food_query')
    def test_order_food(self, mock_order_food_query):
        mock_order_food_query.return_value = self.test_values['order_confirmation']
        data = self.test_values['valid_order_data']

        result = EmployeeServiceHandler.order_food(data)
        expected_result = self.test_values['order_confirmation']

        self.assertEqual(result, expected_result)

    @patch.object(EmployeeQuery, 'fetch_employee_orders_query')
    def test_fetch_employee_orders(self, mock_fetch_employee_orders_query):
        mock_fetch_employee_orders_query.return_value = self.test_values['employee_orders']
        user_id = self.test_values['valid_user_id']

        result = EmployeeServiceHandler.fetch_employee_orders(user_id)
        expected_result = self.test_values['employee_orders']

        self.assertEqual(result, expected_result)

    @patch.object(EmployeeQuery, 'give_feedback_query')
    def test_give_feedback(self, mock_give_feedback_query):
        mock_give_feedback_query.return_value = self.test_values['feedback_confirmation']
        data = self.test_values['valid_feedback_data']

        result = EmployeeServiceHandler.give_feedback(data)
        expected_result = self.test_values['feedback_confirmation']

        self.assertEqual(result, expected_result)

    @patch.object(EmployeeQuery, 'give_feedback_discard_item_query')
    def test_give_feedback_discard_item(self, mock_give_feedback_discard_item_query):
        mock_give_feedback_discard_item_query.return_value = self.test_values['feedback_confirmation']
        data = self.test_values['valid_feedback_discard_data']

        result = EmployeeServiceHandler.give_feedback_discard_item(data)
        expected_result = self.test_values['feedback_confirmation']

        self.assertEqual(result, expected_result)

    @patch.object(EmployeeQuery, 'fetch_discard_item_notifications_query')
    def test_fetch_discard_item_notifications(self, mock_fetch_discard_item_notifications_query):
        mock_fetch_discard_item_notifications_query.return_value = self.test_values['valid_discard_notifications']

        result = EmployeeServiceHandler.fetch_discard_item_notifications()
        expected_result = self.test_values['valid_discard_notifications']

        self.assertEqual(result, expected_result)

    @patch.object(EmployeeQuery, 'update_user_profile_query')
    def test_update_user_profile(self, mock_update_user_profile_query):
        mock_update_user_profile_query.return_value = self.test_values['profile_update_confirmation']
        data = self.test_values['valid_profile_data']

        result = EmployeeServiceHandler.update_user_profile(data)
        expected_result = self.test_values['profile_update_confirmation']

        self.assertEqual(result, expected_result)