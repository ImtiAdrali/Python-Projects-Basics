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
    
    print(f"\n--- All Transactions ({len(transactions)} total) ---")
    print(f"{'Date':<12} {'Type':<10} {'Category':<15} {'Amount':<10} {'Description':<20}")
    print("-" * 75)

    for trans in transactions:
        amount_str = f"${trans["amount"]:.2f}"
        print(f"{trans['date']:<12} {trans['type']:<10} {trans['category']:<15} "
              f"{amount_str:<10} {trans['description']:<20}")
        

def view_monthly_summary():
    """"Display montly summary."""

    transactons = load_transactions()

    if not transactons:
        print("\nNo transactions found.")
        return
    try: 
        year = int(input("Enter year (YYYY): "))
        month = int(input("Enter month (1-12): "))

        summary = get_monthly_summary(transactons, year, month)

        print(f"\n--- Monthly Summary: {summary['month']} ---")
        print(f"Total Income:      ${summary['income']:.2f}")
        print(f"Total Expenses:    ${summary['expense']:.2f}")
        print(f"Net Balance:       ${summary['balance']:.2f}")
        print(f"Transactions:      {summary['transaction_count']}")

        if summary["categories"]:
            print("\nSpending by Category:")
            for cat, data in summary["categories"].items():
                print(f"  {cat}: ${data['total']:.2f} ({data['count']} transactions)")

    except ValueError:
        print("Invalid input. Please enter numeric values for year and month.")


def view_spending_by_category():
    """Display spending breakdown by category."""
    transactions = load_transactions()
    
    if not transactions:
        print("\n📭 No transactions found.")
        return
    
    print("\n--- Spending by Category ---")
    spending = get_spending_by_category(transactions, 'expense')
    
    if not spending:
        print("No expenses recorded.")
        return
    
    total_expenses = sum(data['total'] for data in spending.values())
    
    for cat, data in spending.items():
        percentage = (data['total'] / total_expenses * 100) if total_expenses > 0 else 0
        print(f"{cat:<20} ${data['total']:.2f} ({percentage:.1f}%) - {data['count']} transactions")
    
    print(f"\nTotal Expenses: ${total_expenses:.2f}")

def delete_transaction_menu():
    """Handle deleting a transaction."""
    transactions = load_transactions()
    
    if not transactions:
        print("\n📭 No transactions to delete.")
        return
    
    print("\nRecent Transactions:")
    for i, trans in enumerate(transactions[-10:], 1):
        print(f"{i}. {trans['date']} - {trans['category']} - ${trans['amount']:.2f} (ID: {trans['id']})")
    
    trans_id = input("\nEnter transaction ID to delete: ").strip()
    
    if delete_transaction(trans_id):
        print("✓ Transaction deleted successfully!")
    else:
        print("❌ Transaction not found.")


def main():
    """"Main application loop."""

    print("Welcome to the Personal Finance Tracker!")
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            add_transaction_manu()
        elif choice == "2":
            view_all_transactions()
        elif choice == "3":
            view_monthly_summary()
        elif choice == "4":
            view_spending_by_category()
        elif choice == "5":
            delete_transaction_menu()
        elif choice == "6":
            print("\nThank you for using the Personal Finance Tracker. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please select a valid option (1-6).")

        input("\nPress Enter to continue...")
    

if __name__ == "__main__":
    main()
