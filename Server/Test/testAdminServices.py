import unittest
from unittest.mock import patch
from decimal import Decimal
import json
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from DB_Connection.adminQueries import AdminQuery
from Services.adminServiceHandler import AdminServiceHandler

class TestAdminServiceHandler(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open(os.path.join(os.path.dirname(__file__), 'testValues.json')) as f:
            cls.test_values = json.load(f)

    @patch('DB_Connection.adminQueries.AdminQuery.add_menu_item_query')
    def test_add_menu_item_success(self, mock_add_menu_item_query):
        mock_add_menu_item_query.return_value = {"status": "success"}

        response = AdminServiceHandler.add_menu_item(
            self.test_values['valid_name'], 
            self.test_values['valid_price'], 
            self.test_values['valid_description'], 
            self.test_values['valid_category']
        )
        
        self.assertEqual(response["status"], "success")
        mock_add_menu_item_query.assert_called_once_with(
            self.test_values['valid_name'], 
            self.test_values['valid_price'], 
            self.test_values['valid_description'], 
            self.test_values['valid_category']
        )

    def test_add_menu_item_invalid_name(self):
        response = AdminServiceHandler.add_menu_item(
            self.test_values['invalid_name'], 
            self.test_values['valid_price'], 
            self.test_values['valid_description'], 
            self.test_values['valid_category']
        )
        
        self.assertEqual(response["status"], "error")
        self.assertEqual(response["message"], "Item name cannot be empty.")

    def test_add_menu_item_invalid_price(self):
        response = AdminServiceHandler.add_menu_item(
            self.test_values['valid_name'], 
            self.test_values['invalid_price'], 
            self.test_values['valid_description'], 
            self.test_values['valid_category']
        )
        
        self.assertEqual(response["status"], "error")
        self.assertEqual(response["message"], "Price must be a positive number.")

    @patch('DB_Connection.adminQueries.AdminQuery.delete_menu_item_query')
    def test_delete_menu_item_success(self, mock_delete_menu_item_query):
        mock_delete_menu_item_query.return_value = {"status": "success"}
        
        response = AdminServiceHandler.delete_menu_item(self.test_values['valid_item_id'])
        
        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Menu item deleted successfully.")
        mock_delete_menu_item_query.assert_called_once_with(self.test_values['valid_item_id'])

    def test_delete_menu_item_invalid_id(self):
        response = AdminServiceHandler.delete_menu_item(self.test_values['invalid_item_id'])
        
        self.assertEqual(response["status"], "error")
        self.assertEqual(response["message"], "Invalid item_id. It must be a positive integer.")

    @patch('DB_Connection.adminQueries.AdminQuery.update_menu_item_query')
    def test_update_menu_item_success(self, mock_update_menu_item_query):
        mock_update_menu_item_query.return_value = {"status": "success"}

        response = AdminServiceHandler.update_menu_item(
            self.test_values['valid_item_id'], 
            self.test_values['valid_name'], 
            self.test_values['valid_price'], 
            self.test_values['valid_description'], 
            self.test_values['valid_category']
        )

        self.assertEqual(response["status"], "success")
        self.assertEqual(response["message"], "Menu item updated successfully.")
        mock_update_menu_item_query.assert_called_once_with(
            self.test_values['valid_item_id'], 
            self.test_values['valid_name'], 
            self.test_values['valid_price'], 
            self.test_values['valid_description'], 
            self.test_values['valid_category']
        )

    def test_update_menu_item_invalid_id(self):
        response = AdminServiceHandler.update_menu_item(
            self.test_values['invalid_item_id'], 
            self.test_values['valid_name'], 
            self.test_values['valid_price'], 
            self.test_values['valid_description'], 
            self.test_values['valid_category']
        )
        
        self.assertEqual(response["status"], "error")
        self.assertEqual(response["message"], "Invalid item_id. It must be a positive integer.")

    @patch('DB_Connection.adminQueries.AdminQuery.view_menu_items_query')
    def test_view_menu_items_success(self, mock_view_menu_items_query):
        mock_view_menu_items_query.return_value = [
            (
                self.test_values['valid_item_id'], 
                self.test_values['valid_name'], 
                Decimal(str(self.test_values['valid_price'])), 
                self.test_values['valid_description'], 
                self.test_values['valid_category']
            )
        ]
        
        response = AdminServiceHandler.view_menu_items()
        
        self.assertEqual(response["status"], "success")
        self.assertEqual(len(response["data"]), 1)
        self.assertEqual(response["data"][0]["name"], self.test_values['valid_name'])
        self.assertEqual(response["data"][0]["price"], self.test_values['valid_price'])
        mock_view_menu_items_query.assert_called_once()