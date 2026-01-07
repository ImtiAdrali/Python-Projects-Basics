# Handle saving and loading data from JSON file

import json
import os
from datetime import datetime

DATA_FILE = "data/transactions.json"

def save_transactions(transactions):
    """
    Save transaction to JSON file.

    Args: 
        transactions (list): List of transaction dictionaries
    
    Raises:
        IOError: If file cannot be written
    """

    try:
        os.makedirs("data", exist_ok=True)

        with open(DATA_FILE, "w") as file:
            json.dump(transactions, file, indent=4)
    except IOError as e:
        raise IOError(f"Failed to save transactions: {e}")


def load_transactions():
    """
    Load transactions from JSON file.

    Return:
        list: List of transactions dictionaries

    Raises:
        ValueError: If JSON is corrupt
    """
    
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            transactions = json.load(file)
            return transactions if isinstance(transactions, list) else []
    except json.JSONDecodeError:
        raise ValueError("Corrupted data file. Cannot load transactions.")
    except IOError as e:
        raise IOError(f"Failed to load transactions: {e}")

def add_transaction(transaction):
    """
    Add a new transaction to storage.

    Args:
        transaction (dict): Transaction to add
    """

    transactions = load_transactions()
    transactions.append(transaction)
    save_transactions(transactions)


def delete_transaction(transaction_id):
    """
    Delete a transaction by ID.

    Args: 
        transaction_id (str): ID of transaction to delete

    Return:
        bool: True if deleted, False if not found
    """

    transactions = load_transactions()
    original_length = len(transactions)
    transactions = [t for t in transactions if t["id"] != transaction_id]

    if len(transactions) < original_length:
        save_transactions(transactions)
        return True
    return False


def backup_data():
    """Create a backup of the current data file."""
    if os.path.exists(DATA_FILE):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"data/transactions_backup_{timestamp}.json"

        with open(DATA_FILE, "r") as source:
            with open(backup_file, "w") as backup:
                backup.write(source.read())

        print(f"Backup created: {backup_file}")
        
        








