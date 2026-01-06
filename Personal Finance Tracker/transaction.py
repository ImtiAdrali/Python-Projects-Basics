# Create and validate transactions

from datetime import datetime

def create_transaction(amount, category, transaction_type, description=""):
    """
    Create a transaction dictionary.

    Args:
        amount (float): The amount of the transaction.
        category (str): The category of the transaction (e.g., 'Food', 'Rent', 'Salary', 'Transport').
        transaction_type (str): The type of transaction ('income' or 'expense').
        description (str, optional): A brief description of the transaction.

    Returns:
        dict: Transaction disctionary.

    Raises:
        ValueError: If validation fails
    """

    # Validate amount
    if not isinstance(amount, (int, float)) or amount <= 0:
        raise ValueError("Amount must be a positive number.")
    
    # Validate transaction type
    if transaction_type.lower() not in ("income", "expense"):
        raise ValueError("Transaction type must be either 'income' or 'expense'.")
    
    # Validate category
    if not category or not isinstance(category, str):
        raise ValueError("Category must be a non-empty string.")
    
    # Create transaction dictionary
    transaction = {
        "id": generate_id(),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "amount": round(float(amount), 2),
        "category": category.strip().title(),
        "type": transaction_type.lower(),
        "description": description.strip()
    }

    return transaction


def generate_id():
    """Generate a unique transaction ID using timestamp."""
    return datetime.now().strftime("%y%m%d%H%M%S%f")


def validate_transaction(transaction):
    """
    Validate transaction dictionary has all required fields.
    
    Args:
        transaction (dict): Transaction to validate.

    Returns:
        bool: True if valid, False otherwise.

    Raises:
        ValueError: If validation fails
    """

    required_fields = ["id", "date", "amount", "category", "type"]

    for field in required_fields:
        if field not in transaction:
            raise ValueError(f"Missing required field: {field}")


    if transaction["type"] not in ["income", "expense"]:
        raise ValueError("Invalid transaction type.")
    
    if transaction["amount"] <= 0:
        raise ValueError("Amount must be positive.")
    
    return True
