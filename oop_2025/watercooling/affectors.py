from abc import ABC, abstractmethod

from oop_2025.watercooling.strategy_design import CoolingActions, CoolingAlert


class Affector(ABC):

    @abstractmethod
    def act_on(self, actions: CoolingActions):
        pass


class EmergencyShutter(Affector):

    def act_on(self, actions: CoolingActions):
        if CoolingAlert.CRITICAL_TEMPERATURE in actions.alerts:
            pass
            # cmd.execute('shutdown')


class EmergencyPowerReducer(Affector):

    def __init__(self, cooldown_period_seconds: float):
        self.cooldown_period_seconds = cooldown_period_seconds

    def act_on(self, actions: CoolingActions):
        if CoolingAlert.HIGH_TEMPERATURE in actions.alerts:
            self.reduce_cpu_frequency()

        # todo -- if longer than self.cooldown_period_seconds in redcuced frequency -- restore it ...

    def reduce_cpu_frequency(self):
        pass
        # cmd.execute('cpupower frequency-set -u 3000') # reduce max frequency of CPU



