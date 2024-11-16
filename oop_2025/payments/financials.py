from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from pydantic import BaseModel

from oop_2025.payments.bank_errors import AccountNotFoundError, InvalidCurrencyError, InsufficientFundsError


class User(BaseModel):
    id: UUID
    name: str
    email: str


class Account(BaseModel):
    account_id: UUID
    owner_id: UUID
    balance: float
    currency: str = 'PLN'


class Payment(BaseModel):
    payment_id: UUID
    account_source: UUID
    account_target: UUID
    amount: float
    currency: str


class IBank(ABC):
    # każda klasa implementująca ten interfejs jest bankiem

    @abstractmethod
    def create_account(self, user: User) -> Account:
        pass

    @abstractmethod
    def cash_transfer(self, account_id: UUID, amount: float, currency: str):
        """
        Wpłata cash na konto.

        :param account_id:
        :param amount:
        :param currency:
        :return:
        """
        pass

    @abstractmethod
    def payment(self, account_source: UUID, account_target: UUID, amount: float, currency: str) -> Payment:
        """
        Przelew z account_source do account_target.
        :param account_source:
        :param account_target:
        :param amount:
        :param currency:
        :return:
        """
        pass

    @abstractmethod
    def get_account(self, account_id: UUID) -> Account:
        """
        Zwraca informacje o koncie.
        Note: powinna to być _kopia_ informacji z banku.

        :param account_id:
        :return:
        """
        pass


class SimpleBank(IBank):

    def __init__(self, default_currency="USD"):
        self.default_currency = default_currency
        self.accounts: dict[UUID, Account] = {}  # account_id -> Account   #todo: make private

    def create_account(self, user: User, currency=None) -> Account:
        if currency is None:
            currency = self.default_currency
        account = Account(account_id=uuid4(), owner_id=user.id, balance=0, currency=currency)
        self.accounts[account.account_id] = account
        return account

    def cash_transfer(self, account_id: UUID, amount: float, currency: str):
        if account_id not in self.accounts:
            raise AccountNotFoundError(account_id=account_id)

        acc = self.accounts[account_id]

        if acc.currency != currency:
            raise InvalidCurrencyError(currency=currency)

        acc.balance += amount

    def payment(self, account_source: UUID, account_target: UUID, amount: float, currency: str) -> Payment:
        if account_source not in self.accounts:
            raise AccountNotFoundError(account_id=account_source)
        if account_target not in self.accounts:
            raise AccountNotFoundError(account_id=account_target)

        acc_s = self.accounts[account_source]
        acc_t = self.accounts[account_target]

        if acc_s.currency != currency:
            raise InvalidCurrencyError(currency=currency)
        if acc_t.currency != currency:
            raise InvalidCurrencyError(currency=currency)

        if acc_s.balance < amount:
            raise InsufficientFundsError(account_id=acc_s.account_id,
                                         requested_amount=amount,
                                         available_balance=acc_s.balance)

        payment = Payment(payment_id=uuid4(),
                          account_source=acc_s.account_id,
                          account_target=acc_t.account_id,
                          amount=amount,
                          currency=currency)

        acc_s.balance -= amount
        acc_t.balance += amount

        return payment

    def get_account(self, account_id: UUID) -> Account:
        if account_id not in self.accounts:
            raise AccountNotFoundError(account_id=account_id)

        acc = self.accounts[account_id].model_copy()
        return acc


if __name__ == '__main__':
    user1 = User(id=uuid4(), name='Xiaoli', email='<EMAIL>')
    print(user1)

    acc1 = Account(account_id=uuid4(), owner_id=user1.id, balance=100, currency='PLN')
    print(acc1)
