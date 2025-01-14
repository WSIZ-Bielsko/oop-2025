from abc import ABC, abstractmethod
from enum import Enum
from statistics import mean

from pydantic import BaseModel


class CoolingAlert(Enum):
    NO_DATA_RECORDED = 0
    HIGH_TEMPERATURE = 1
    LOW_TEMPERATURE = 2
    CRITICAL_TEMPERATURE = 3
    LOW_FLOW_RATE = 4


class CoolingData(BaseModel):
    temps: list[float]
    flow_rate: float = 1.0
    cpu_power: float = 4000  # in W or MHz


class CoolingActions(BaseModel):
    desired_flow_rate: float
    desired_cpu_power: float
    alerts: list[CoolingAlert]


class StrategyConfig(BaseModel):
    # alerts
    low_temperature: float = 15
    high_temperature: float = 55
    critical_temperature: float = 70
    low_flow_rate: float = 0.1  # of maximum

    # CPU
    max_cpu_power: float = 4000
    min_cpu_power: float = 800

    # flow
    max_flow_rate: float = 1.0
    min_flow_rate: float = 0.1


class Strategy(ABC):

    @abstractmethod
    def configure(self, config: StrategyConfig = StrategyConfig()):
        pass

    @abstractmethod
    def update_state(self, data: CoolingData):
        pass

    @abstractmethod
    def get_action(self) -> CoolingActions:
        pass


class MyStrategy(Strategy):

    def __init__(self):
        self.config = StrategyConfig()

    def configure(self, config: StrategyConfig = StrategyConfig()):
        self.config = config

    def update_state(self, data: CoolingData):
        pass

    def get_action(self) -> CoolingActions:
        pass


class ReferenceStrategy(Strategy):

    def __init__(self):
        self.config = StrategyConfig()
        self.mean_temps = []
        self.max_temps = []
        self.epoch = 0
        self.cpu_power = 0.  # no info
        self.flow_rate = 0.  # no info

    def configure(self, config: StrategyConfig = StrategyConfig()):
        self.config = config

    def update_state(self, data: CoolingData):
        avg_tmp = mean(data.temps)
        self.mean_temps.append(avg_tmp)
        self.max_temps.append(max(data.temps))

        self.mean_temps = self.mean_temps[-5:]  # gather some history
        self.max_temps = self.max_temps[-5:]

        # update system state
        self.cpu_power = data.cpu_power
        self.flow_rate = data.flow_rate

        self.epoch += 1

    def get_action(self) -> CoolingActions:
        if self.epoch == 0:
            # nothing measured so far
            return CoolingActions(alerts=[CoolingAlert.NO_DATA_RECORDED],
                                  desired_flow_rate=0,
                                  desired_cpu_power=0)

        alerts = []
        desired_cpu_power = self.cpu_power
        desired_flow_rate = self.flow_rate

        if max(self.max_temps) > self.config.critical_temperature:
            alerts.append(CoolingAlert.CRITICAL_TEMPERATURE)
            desired_cpu_power = self.config.min_cpu_power
        elif max(self.max_temps) > self.config.high_temperature:
            alerts.append(CoolingAlert.HIGH_TEMPERATURE)
            desired_cpu_power = min(self.cpu_power, self.config.max_cpu_power * 0.9)

        if min(self.mean_temps) < self.config.low_temperature:
            alerts.append(CoolingAlert.LOW_TEMPERATURE)
            desired_cpu_power = self.config.max_cpu_power

        action = CoolingActions(desired_flow_rate=desired_flow_rate,
                                desired_cpu_power=desired_cpu_power,
                                alerts=alerts)
        return action


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
