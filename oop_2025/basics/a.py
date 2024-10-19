from pydantic import BaseModel

"""
Klasy danych

Klasy

Klasy abstrakcyjne / interfejsy

"""


class Client(BaseModel):
    first_name: str  # pola (atrybuty)
    last_name: str
    age: int
    email: str
    pesel: str


if __name__ == '__main__':
    c1 = Client(first_name='John', last_name='Stewart', age=25, email='<EMAIL1>', pesel='P1')  # instancje
    c2 = Client(first_name='Jane', last_name='Doe', age=30, email='<EMAIL2>', pesel='P2')

    print(c1)

    clients = [c1, c2]
    print(clients)

    # first_names = []
    # last_names = []
    # ages = []
    # emails = []

    for c in clients:
        if c.age == 'P1':
            c.age += 1

    for c in clients:
        print(c)


