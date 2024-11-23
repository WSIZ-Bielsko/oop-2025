import datetime
from abc import ABC, abstractmethod
from collections import defaultdict
from uuid import uuid4, UUID

from pydantic import BaseModel

from oop_2025.payments.bank_errors import AccountNotFoundError
from oop_2025.payments.financials import User, Account, Payment, IBank, SimpleBank

"""


"""


class AmericanUser(User):
    ssn: str


class FATCACompliantBank(ABC):

    @abstractmethod
    def get_american_accounts(self) -> list[Account]:
        """
        All accounts of AmericanUser's in the bank (with _full_ details)
        :return:
        """
        pass

    @abstractmethod
    def get_american_payments(self) -> list[Payment]:
        """
        All Payment instnaces related to (source or target) AmericanAccounts
        :return:
        """
        pass


# ------------- IMPLEMENTATIONS

class Transfer(BaseModel):
    user_id: UUID
    amount: float
    currency: str
    executed_at: datetime.datetime


class SimpleAmericanBank(IBank, FATCACompliantBank):

    def __init__(self):
        self.bank = SimpleBank()
        self.amercians: dict[UUID, AmericanUser] = dict()
        self.deleted_accounts: dict[UUID, Account] = dict()  # future feature to be implemented

        # list of all transfer by given american UUID
        self.american_transfers: dict[UUID, list[Transfer]] = defaultdict(lambda: [])
        self.american_payments: dict[UUID, list[Payment]] = defaultdict(lambda: [])

    def create_account(self, user: User) -> Account:
        print(f'creating account for {user.name}')
        if isinstance(user, AmericanUser):
            self.amercians[user.id] = user
            print(f'stored info on {user.name} with ssn {user.ssn}; his operations will be recorded!')
        return self.bank.create_account(user)

    def get_account(self, account_id: UUID) -> Account:
        return self.bank.get_account(account_id)

    def cash_transfer(self, account_id: UUID, amount: float, currency: str):
        account = self.bank.get_account(account_id)
        if not account:
            raise AccountNotFoundError(account_id)
        if account.owner_id in self.amercians:
            t = Transfer(user_id=account.owner_id, amount=amount, currency=currency,
                         executed_at=datetime.datetime.now())
            self.american_transfers[account.owner_id].append(t)

        return self.bank.cash_transfer(account_id, amount, currency)

    def payment(self, account_source: UUID, account_target: UUID, amount: float, currency: str) -> Payment:

        payment = self.bank.payment(account_source, account_target, amount, currency)

        acc_source = self.bank.get_account(account_source)
        acc_target = self.bank.get_account(account_target)

        if acc_source.owner_id in self.amercians:
            self.american_payments[acc_source.owner_id].append(payment)
        if acc_target.owner_id in self.amercians:
            self.american_payments[acc_target.owner_id].append(payment)

        return payment

    # FATCA
    def get_american_accounts(self) -> list[Account]:
        accounts = list(self.amercians.values())
        return accounts

    def get_american_payments(self) -> list[Payment]:
        pass


def write_email(user: User):
    return {'address': user.email, 'title': 'important info', 'body': f'Hello {user.name}!'}


if __name__ == '__main__':
    u = User(id=uuid4(), name='Kenji', email='kenji@kajima.jp')
    ua = AmericanUser(id=uuid4(), name='Bill', email='bill@microsoft.com', ssn='123-56-6789')

    # print(u)
    # print(ua)
    #
    # print(write_email(u))
    # print(write_email(ua))
    #
    # print(isinstance(u, User))
    # print(isinstance(ua, User))

    bank = SimpleAmericanBank()
    bank.create_account(ua)
    bank.create_account(u)
