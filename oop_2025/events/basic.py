from abc import ABC, abstractmethod

from pydantic import BaseModel


class Payload(ABC, BaseModel):
    pass


class StringPayload(Payload):
    data: str


class Event(BaseModel):
    id: int
    type: str
    payload: Payload


class EventDriven(ABC):

    @abstractmethod
    def on_event(self, event: Event):
        pass


class Printer(EventDriven):

    def on_event(self, event: Event):
        print(event.payload)


class Logger(EventDriven):
    def __init__(self):
        self.log = []

    def on_event(self, event: Event):
        self.log.append(event.payload)

    def flush(self):
        print(self.log)
        self.log = []



if __name__ == '__main__':
    e = Event(id=1, type='calendar', payload=StringPayload(data='abra kadabra'))

    p1 = Printer()
    p2 = Printer()
    ll = Logger()

    p1.on_event(e)
    p2.on_event(e)
    ll.on_event(e)

    ll.flush()
    ll.flush()
