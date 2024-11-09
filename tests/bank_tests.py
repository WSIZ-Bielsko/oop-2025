import pytest
from uuid import UUID, uuid4
from decimal import Decimal
from typing import Optional

from oop_2025.basics.bank_errors import InsufficientFundsError, InvalidCurrencyError
from oop_2025.payments.financials import User, SimpleBank


@pytest.fixture
def bank():
    return SimpleBank()


@pytest.fixture
def test_user():
    return User(id=uuid4(), name="Test User", email="<EMAIL>")


def test_works():
    a = 12
    assert a == 12


def test_create_account(bank, test_user):
    account = bank.create_account(test_user)
    assert account is not None
    assert account.owner_id == test_user.id
    assert account.balance == Decimal('0')


def test_cash_transfer(bank, test_user):
    account = bank.create_account(test_user)
    amount = 1000.0

    result = bank.cash_transfer(
        account_id=account.id,
        amount=amount,
        currency="USD"
    )
    assert result is True
    assert account.balance == Decimal(str(amount))


def test_payment_between_accounts(bank):
    source_user = User(id="source123", name="Source User")
    target_user = User(id="target123", name="Target User")

    source_account = bank.create_account(source_user)
    target_account = bank.create_account(target_user)

    # Add money to source account
    bank.cash_transfer(source_account.id, 1000.0, "USD")

    result = bank.payment(
        account_source=source_account.id,
        account_target=target_account.id,
        amount=500.0,
        currency="USD"
    )
    assert result is True
    assert source_account.balance == Decimal('500')
    assert target_account.balance == Decimal('500')


def test_payment_insufficient_funds(bank, test_user):
    source_account = bank.create_account(test_user)
    target_account = bank.create_account(User(id="target", name="Target"))

    with pytest.raises(InsufficientFundsError):
        bank.payment(
            account_source=source_account.id,
            account_target=target_account.id,
            amount=100.0,
            currency="USD"
        )


def test_invalid_currency(bank, test_user):
    account = bank.create_account(test_user)

    with pytest.raises(InvalidCurrencyError):
        bank.cash_transfer(
            account_id=account.id,
            amount=100.0,
            currency="INVALID"
        )
