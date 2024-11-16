from uuid import uuid4

import pytest

from oop_2025.payments.bank_errors import InsufficientFundsError, InvalidCurrencyError
from oop_2025.payments.financials import User, SimpleBank, Account


@pytest.fixture
def bank():
    return SimpleBank(default_currency="USD")


@pytest.fixture
def test_user():
    return User(id=uuid4(), name="Test User", email="<EMAIL>")


@pytest.fixture
def test_account(bank, test_user):
    acc = bank.create_account(user=test_user, currency="USD")
    return acc


def test_works():
    a = 12
    assert a == 12


def test_create_account(bank, test_user):
    account = bank.create_account(test_user)
    assert account is not None
    assert account.owner_id == test_user.id
    assert account.balance == 0


def test_get_account(bank, test_account):
    acc = bank.get_account(test_account.account_id)
    initial_balance = acc.balance

    assert acc.account_id == test_account.account_id
    acc.balance = 666.66

    acc2 = bank.get_account(test_account.account_id)
    assert acc2.balance == initial_balance


def test_cash_transfer(bank, test_user):
    account = bank.create_account(test_user)
    amount = 1000.0

    bank.cash_transfer(
        account_id=account.account_id,
        amount=amount,
        currency="USD"
    )

    assert account.balance == amount


def test_payment_between_accounts(bank):
    source_user = User(id=uuid4(), name="Source User", email="<EMAIL>")
    target_user = User(id=uuid4(), name="Target User", email="<EMAIL>")

    source_account = bank.create_account(source_user, currency="USD")
    target_account = bank.create_account(target_user, currency="USD")

    # Add money to source account
    bank.cash_transfer(source_account.account_id, 1000.0, "USD")

    pment = bank.payment(
        account_source=source_account.account_id,
        account_target=target_account.account_id,
        amount=100.0,
        currency="USD"
    )
    assert pment is not None
    assert pment.account_source == source_account.account_id
    assert pment.account_target == target_account.account_id
    assert pment.amount == 100.0
    assert pment.currency == "USD"

    assert source_account.balance == 900
    assert target_account.balance == 100


def test_payment_insufficient_funds(bank, test_user):
    source_account = bank.create_account(test_user)
    target_account = bank.create_account(User(id=uuid4(), name="Target", email="<EMAIL>"))

    bank.cash_transfer(source_account.account_id, 50.0, "USD")

    with pytest.raises(InsufficientFundsError):
        bank.payment(
            account_source=source_account.account_id,
            account_target=target_account.account_id,
            amount=100.0,
            currency="USD"
        )

    assert bank.get_account(source_account.account_id).balance == 50.0
    assert bank.get_account(target_account.account_id).balance == 0


def test_invalid_currency(bank, test_user):
    account = bank.create_account(test_user)

    with pytest.raises(InvalidCurrencyError):
        bank.cash_transfer(
            account_id=account.account_id,
            amount=100.0,
            currency="INVALID"
        )
