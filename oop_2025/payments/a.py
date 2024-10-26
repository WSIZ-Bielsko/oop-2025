from abc import ABC, abstractmethod
from uuid import UUID, uuid4

from pydantic import BaseModel


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
        pass

    @abstractmethod
    def payment(self, account_source: UUID, account_target: UUID, amount: float, currency: str) -> Payment:
        pass


class SimpleBank(IBank):

    def __init__(self):
        pass

    def create_account(self, user: User) -> Account:
        # todo
        pass

    def cash_transfer(self, account_id: UUID, amount: float, currency: str):
        # todo
        pass

    def payment(self, account_source: UUID, account_target: UUID, amount: float, currency: str) -> Payment:
        # todo
        pass


if __name__ == '__main__':
    user1 = User(id=uuid4(), name='Xiaoli', email='<EMAIL>')
    print(user1)

    acc1 = Account(account_id=uuid4(), owner_id=user1.id, balance=100, currency='PLN')
    print(acc1)
