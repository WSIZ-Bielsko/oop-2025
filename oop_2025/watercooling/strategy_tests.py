from _pytest.fixtures import fixture

from oop_2025.watercooling.strategy_design import MyStrategy, StrategyConfig, CoolingData, CoolingAlert, ReferenceStrategy


# TESTS WHICH DEFINE THE PROBLEM

@fixture
def strategy():
    s = ReferenceStrategy()  # substitute your strategy here for testing!
    s.configure(StrategyConfig(high_temperature=50,
                               critical_temperature=70,
                               low_flow_rate=0.1,
                               min_cpu_power=800,
                               max_cpu_power=4000,
                               min_flow_rate=0.1,
                               max_flow_rate=1.0))
    return s


def test_emit_temperature_high_alert(strategy):
    s = strategy
    temps = [30, 30, 40, 50, 60]
    for temp in temps:
        s.update_state(CoolingData(temps=[temp]))

    action = s.get_action()

    assert CoolingAlert.HIGH_TEMPERATURE in action.alerts


def test_critical_downtacts_cpu(strategy):
    s = strategy
    s.update_state(CoolingData(temps=[75]))
    action = s.get_action()

    assert CoolingAlert.CRITICAL_TEMPERATURE in action.alerts
    assert action.desired_cpu_power == s.config.min_cpu_power


def test_history_plays_role(strategy):
    s = strategy
    for t in [75, 50, 50, 50, ]:
        s.update_state(CoolingData(temps=[t], cpu_power=s.config.max_cpu_power))
    action = s.get_action()
    assert CoolingAlert.CRITICAL_TEMPERATURE in action.alerts
    assert action.desired_cpu_power == s.config.min_cpu_power


def test_very_old_temperatures_play_no_role(strategy):
    s = strategy  # alias
    for t in [75, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]:
        s.update_state(CoolingData(temps=[t], cpu_power=s.config.max_cpu_power))
    action = s.get_action()
    assert CoolingAlert.CRITICAL_TEMPERATURE not in action.alerts
    assert action.desired_cpu_power == s.config.max_cpu_power


def test_asking_action_before_data_produces_alert(strategy):
    s = strategy
    action = s.get_action()
    assert CoolingAlert.NO_DATA_RECORDED in action.alerts


def test_single_high_temperature_produces_alert(strategy):
    s = strategy
    s.update_state(CoolingData(temps=[60, 30, 30, 30]))  # single update, many temperatures (many core temps,, or memory or ...)
    action = s.get_action()
    assert CoolingAlert.HIGH_TEMPERATURE in action.alerts


def test_high_temps_cannot_run_full_power(strategy):
    s = strategy
    config = strategy.config

    high = config.high_temperature

    for t in [high + 1, high + 1, high + 1]:
        s.update_state(CoolingData(temps=[t]))

    action = s.get_action()
    assert action.desired_cpu_power < config.max_cpu_power
