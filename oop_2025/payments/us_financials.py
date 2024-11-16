from uuid import uuid4

from oop_2025.payments.financials import User

"""


"""


class AmericanUser(User):
    ssn: str


def write_email(user: User):
    return {'address': user.email, 'title': 'important info', 'body': f'Hello {user.name}!'}


if __name__ == '__main__':
    u = User(id=uuid4(), name='John', email='john@gmail.com')

    ua = AmericanUser(id=uuid4(), name='Bill', email='bill@microsoft.com', ssn='123-56-6789')

    print(u)
    print(ua)

    print(write_email(u))
    print(write_email(ua))

    print(isinstance(u, User))
    print(isinstance(ua, User))
