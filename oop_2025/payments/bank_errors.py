from uuid import UUID


class BankException(Exception):
    """Base exception class for bank operations"""
    pass


class InsufficientFundsError(BankException):
    """Raised when an account has insufficient funds for a transaction"""

    def __init__(self, account_id: UUID, requested_amount: float, available_balance: float):
        self.account_id = account_id
        self.requested_amount = requested_amount
        self.available_balance = available_balance
        super().__init__(
            f"Insufficient funds in account {account_id}. "
            f"Requested: {requested_amount}, Available: {available_balance}"
        )


class InvalidCurrencyError(BankException):
    """Raised when an invalid currency code is provided"""

    def __init__(self, currency: str):
        self.currency = currency
        super().__init__(f"Invalid currency code: {currency}")


class AccountNotFoundError(BankException):
    """Raised when an account cannot be found"""

    def __init__(self, account_id: UUID):
        self.account_id = account_id
        super().__init__(f"Account not found: {account_id}")
