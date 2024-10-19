from datetime import date

from pydantic import BaseModel


class Event(BaseModel):
    name: str
    score: int
    date: date

def get_event() -> Event:
    return Event(name='Kadabra', score=12, date=date(year=2024, month=10, day=19))

if __name__ == '__main__':
    e = get_event()
    print(e.date)