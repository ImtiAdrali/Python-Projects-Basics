# Unit tests for Personal Finance Tracker

import unittest
import os
import json
from transaction import create_transaction, validate_transaction
from storage import save_transaction, load_transaction, DATA_FILE
from analytics import calculate_total_by_type, calculate_balance, get_transaction_by_category, filter_by_month

class TestTransaction(unittest.TestCase):
    
    def test_create_valid_transaction(self):
        """ Test creating a valid transaction"""
        trans = create_transaction(50.0, "Food", "expense", "Lunch")

        self.assertEqual(trans["amount"] == 50.0)
        self.assertEqual("category", "Food")
        self.assertEqual("type", "expense")
        self.assertIn("id", trans)
        self.assertIn("date", trans)

    
    def test_create_transaction_invalid_amount(self):
        """ Test that negative amount raises error."""

        with self.assertRaises(ValueError):
            create_transaction(-10, "Food", "expense")


    def test_create_transaction_invalid_type(self):
        """ Test that invalid type raises error."""

        with self.assertRaises(ValueError):
            create_transaction(50, "Food", "invalid")

    
    def test_validate_transaction(self):
        """ Test trasnsaction validation. """

        trans = create_transaction(100, "Salary", "income")
        self.assertTrue(validate_transaction(trans))



