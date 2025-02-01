from time import sleep

from loguru import logger

from oop_2025.watercooling.affectors import Affector
from oop_2025.watercooling.sensors import ThermalSensor, FlowSensor, Sensor
from oop_2025.watercooling.strategy_design import Strategy, CoolingData, ReferenceStrategy


class WaterCoolingController:

    def __init__(self, base_strategy: Strategy):
        self.base_strategy = base_strategy
        self.strategy = base_strategy
        self.affectors = []

    def attach_affector(self, affector: Affector):
        self.affectors.append(affector)

    def _attach_thermal_sensor(self, sensor: ThermalSensor):
        pass

    def _attach_flow_sensor(self, sensor: FlowSensor):
        pass

    def attach_sensor(self, sensor: Sensor):
        if isinstance(sensor, ThermalSensor):
            self._attach_thermal_sensor(sensor)
        if isinstance(sensor, FlowSensor):
            self._attach_flow_sensor(sensor)

    def run(self):
        while True:
            temperatures = self.measure_temperatures()
            flows = self.measure_flow_rate()

            self.strategy.update_state(data=CoolingData(temps=temperatures, flow_rate=flows, cpu_power=4000))
            actions = self.strategy.get_action()

            for affector in self.affectors:
                affector.action(actions)

            sleep(2.0)

    def measure_temperatures(self) -> tuple[float, ...]:
        # todo -- attach temperature sensors (like affectors)
        return 30., 30., 30.

    def measure_flow_rate(self):
        # todo -- attach flow sensors (like affectors)
        return 0.7


if __name__ == '__main__':
    strategy = ReferenceStrategy()
    controller = WaterCoolingController(strategy)

