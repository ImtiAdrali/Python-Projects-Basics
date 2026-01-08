# Calculate summary statistics for personal finance data.

from datetime import datetime
from collections import defaultdict

def calculate_total_by_type(transactions, transaction_type):
    """
    Calculate total fro income and expense.

    Args:
        transactions (list): List of trasactions.
        transaction_type (str): 'income' or 'expense'.

    Returns:
        float: Total amount
    """

    total = sum(t["amount"] for t in transactions if t["type"] == transaction_type)
    return round(total, 2)


def calculate_balance(transactions):
    """"
    Calculate total for income and expense

    Args: 
        transactions (list): List of trasactions.

    Returns:
        float: Net balance
    """
    income = calculate_total_by_type(transactions, "income")
    expenses = calculate_total_by_type(transactions, "expense")
    return round(income - expenses, 2)


def get_transactions_by_category(transactions):
    """"
    Ground transactions by category with totals.

    Args:
        transactions (list): List of trasactions.

    Returns:
        dict: {category: {'total': amount, 'count': num_transactions}}
    """

    categories = defaultdict(lambda: {"total": 0, "count": 0})

    for trans in transactions:
        cat = trans["category"]
        categories[cat]["total"] += trans["amount"]
        categories[cat]["count"] += 1
        categories[cat]["total"] = round(categories[cat]["total"], 2)

    return dict(categories)


def filter_by_month(transactions, year, month):
    """
    Filter transactions by specific month and year.

    Args:
        transactions (list): List of transactions.
        year (int): Year to filter.
        month (int): Month to filter.

    Returns: 
        list: Filtered transactions.
    """

    filtered = []
    for trans in transactions:
        trans_date = datetime.strptime(trans["date"], "%Y-%m-%d")
        if trans_date.year == year and trans_date.month == month:
            filtered.append(trans)
    
    return filtered


def get_monthly_summary(transactions, year, month):
    """"
    Generate summary for a specific month.

    Args:
        transactions (list): List of transactions.
        year (int): Year
        month (int): Month.

    Returns:
        dict: Summary with income, expense, balance, categories
    """

    monthly_trans = filter_by_month(transactions, year, month)

    return {
        "month": f"{year}-{month:02d}",
        "income": calculate_total_by_type(monthly_trans, "income"),
        "expense": calculate_total_by_type(monthly_trans, "expense"),
        "balance": calculate_balance(monthly_trans),
        "categories": get_transactions_by_category(monthly_trans),
        "transaction_count": len(monthly_trans)
    }


def get_spending_by_category(transactions, transaction_type="expense"):
    """
    Get spending or income breakdown by category.

    Args:
        transactions (list): List of transactions.
        transaction_type (str): 'income' or 'expense'.

    Return: 
        dict: Category totals sorted by amount.
    """
    filtered = [t for t in transactions if t["type"] == transaction_type]
    categories = get_transactions_by_category(filtered)

    sorted_categories = dict(sorted(categories.items(), key=lambda x: x[1]["total"], reverse=True))
    return sorted_categories