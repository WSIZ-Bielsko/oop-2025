from abc import ABC, abstractmethod
from collections.abc import *


class Sensor(ABC):
    """
    All sensors must inherit from this class.
    """


class ThermalSensor(Sensor):

    @abstractmethod
    def get_temperatures(self) -> list[float]:
        pass


class FlowSensor(Sensor):
    @abstractmethod
    def get_flow_rate_L_per_h(self) -> float:
        pass


class SimpleThermo(ThermalSensor):

    def __init__(self):
        self.data = [10, 4, 0, 255, 250, 252, 1, 4]
        self.idx = -1

    def get_temperatures(self) -> list[float]:
        self.idx += 1
        return [self.data[self.idx]]


class DummyFlowSensor(FlowSensor):
    def get_flow_rate_L_per_h(self) -> float:
        return 100.


class EnhancedSimpleThermo(SimpleThermo):

    def __init__(self):
        super().__init__()
        self.previous_reading = None

    def get_temperatures(self) -> list[float]:
        temps = super().get_temperatures()
        assert len(temps) == 1  # we assume the underlying Sensor returns 1 temperature only
        temp = temps[0]
        if not self.previous_reading:
            self.previous_reading = temp
        selected_temp = temp
        delta = abs(temp - self.previous_reading)
        for i in range(-10, 11):
            candidate_temp = temp - i * 256
            if abs(candidate_temp - self.previous_reading) < delta:
                delta = abs(candidate_temp - self.previous_reading)
                selected_temp = candidate_temp
        self.previous_reading = selected_temp
        return [selected_temp]


def test_enhancement0():
    es = EnhancedSimpleThermo()
    es.data = [10, 4]
    results = [es.get_temperatures()[0] for i in range(len(es.data))]
    # print(results)
    assert results == [10, 4]


def test_enhancement1():
    es = EnhancedSimpleThermo()
    es.data = [10, 4, 250]
    results = [es.get_temperatures()[0] for i in range(len(es.data))]
    # print(results)
    assert results == [10, 4, 250 - 256]


def test_enhancement2():
    es = EnhancedSimpleThermo()
    es.data = [10, 4, 250, 245, 1, 2]
    results = [es.get_temperatures()[0] for i in range(len(es.data))]
    # print(results)
    assert results == [10, 4, 250 - 256, 245 - 256, 1, 2]


def test_enhancement3():
    es = EnhancedSimpleThermo()
    es.data = [10, 4, 250, 150, 100, 50, 20, 250, 240]
    results = [es.get_temperatures()[0] for i in range(len(es.data))]
    # print(results)
    assert results == [10, 4, 250 - 256, 150 - 256, 100 - 256, 50 - 256, 20 - 256, 250 - 2 * 256, 240 - 2 * 256]


if __name__ == '__main__':
    s = EnhancedSimpleThermo()
    print(s.get_temperatures())
