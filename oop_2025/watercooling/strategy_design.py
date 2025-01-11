from abc import ABC, abstractmethod

from pydantic import BaseModel


class CoolingData(BaseModel):
    temps: list[float]
    flow_rate: float
    cpu_power: float  # in W or MHz


class CoolingActions(BaseModel):
    desired_flow_rate: float
    desired_cpu_power: float


class Strategy(ABC):

    @abstractmethod
    def update_state(self, data: CoolingData):
        pass

    @abstractmethod
    def get_action(self) -> CoolingActions:
        pass

class MyStrategy(Strategy):

    def update_state(self, data: CoolingData):
        pass

    def get_action(self) -> CoolingActions:
        pass


def test_easy():
    data = CoolingData(temps=[20], flow_rate=0.5, cpu_power=0.5)


def test_challenge1():
    temp = 30
    power = 5.0
    flow_rate = 0.5

    strategy = MyStrategy()

    for i in range(40):
        data = CoolingData(temps=[temp], flow_rate=flow_rate, cpu_power=power)
        strategy.update_state(data)
        actions = strategy.get_action()
        power = actions.desired_cpu_power
        flow_rate = actions.desired_flow_rate
        temp += power - flow_rate

    # adjust your strategy to get temperature ~= 20C after this loop
    assert abs(temp - 20) < 1

if __name__ == '__main__':
    pass
