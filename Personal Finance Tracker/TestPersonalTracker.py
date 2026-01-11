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


class TestStorage(unittest.TestCase):

    def setUp(self):
        """ Set up test by removing test data file."""

        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def tearDown(self):
        """ Clean up test data file. """

        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_save_and_load_transaction(self):
        """ Test saving and loading transactions."""
        trans1 = create_transaction(50, "Food", "expense")
        trans2 = create_transaction(1000, "Salary", "income")

        save_transaction([trans1, trans2])
        loaded = load_transaction()

        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]["amount"], 50)
        self.assertEqual(loaded[1]["amount"], 1000)


    def test_load_empty_file(self):
        """ Test loading when no file exists. """

        loaded = load_transaction()
        self.assertEqual(loaded, [])

class TestAnalytics(unittest.TestCase):

    def setUp(self):
        """ Create sample transactions for testing. """

        self.transactions = [
            create_transaction(1000, "Salary", "income"),
            create_transaction(50, "Food", "expense"),
            create_transaction(30, "Transport", "expense"),
            create_transaction(20, "Food", "expense"),
        ]

    def test_calculate_total_income(self):
        """ Test calculating total income."""

        total = calculate_total_by_type(self.transactions, "income")
        self.assertEqual(total, 1000)
    

    def test_calculate_total_expenses(self):
        """ Test calculating total expenses."""

        total = calculate_total_by_type(self.transactions, "expense")
        self.assertEqual(total, 100)

    
    def test_calculate_balance(self):
        """ Test balance calculation. """

        balance = calculate_balance(self.transactions)
        self.assertEqual(balance, 900)

    
    def test_get_transactions_by_category(self):
        """ Test grouping by category. """

        categories = get_transaction_by_category(self.transactions)

        self.assertEqual(categories["Food"]["total"], 70)
        self.assertEqual(categories["Food"]["count"], 2)
        self.assertEqual(categories["transport"]["total"], 30)


if __name__ == "__main__":
    unittest.main()










