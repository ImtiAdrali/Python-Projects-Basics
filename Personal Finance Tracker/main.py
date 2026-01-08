# User intrface and application flow

import sys
from datetime import datetime
from transaction import create_transaction
from storage import add_transaction, load_transactions, delete_transaction
from analytics import calculate_balance, calculate_total_by_type, get_spending_by_category, get_monthly_summary

def display_menu():
    """" Display main manu options."""
    print("\n" + "="*50)
    print(" PERSONAL FINANCE TRACKER ")
    print("="*50)
    print("1. Add Transaction")
    print("2. View All Transactions")
    print("3. View Monthly Summary")
    print("4. View Spending by Category")
    print("5. Delete Transaction")
    print("6. Exit")
    print("="*50)

def add_transaction_manu():
    """Handle adding a new transactions."""

    print("\n---Add New Transaction---")
    try:
        transaction_type = input("Type (income/expense): ").strip().lower()
        if transaction_type not in ["income", "expense"]:
            print("Invalid transaction type. Must be 'income' or 'expense'.")
            return
        
        amount = float(input("Amount: $"))
        category = input("Category: ").strip()
        description = input("Description (optional): ").strip()

        transaction = create_transaction(amount, category, transaction_type, description)
        add_transaction(transaction)

        print(f"Transaction added successfully! (ID: {transaction['id']})")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def view_all_transactions():
    """"Display all transactions."""

    transactions = load_transactions()

    if not transactions:
        print("\nNo transactions found.")
        return
    
    