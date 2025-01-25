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


def test_zero_flow_rate_emits_warning_and_sets_cpu_power_to_minimum(strategy):
    s = strategy
    config = strategy.config

    s.update_state(CoolingData(temps=[30], cpu_power=config.min_cpu_power + 100, flow_rate=0))

    action = s.get_action()

    assert CoolingAlert.LOW_FLOW_RATE in action.alerts
    assert action.desired_cpu_power == s.config.min_cpu_power


def test_pump_cavitation_detection(strategy):
    s = strategy
    # Simulating cavitation with erratic flow rates and temps
    s.update_state(CoolingData(temps=[35], flow_rate=1.2))
    s.update_state(CoolingData(temps=[34], flow_rate=0.8))
    s.update_state(CoolingData(temps=[36], flow_rate=1.3))
    action = s.get_action()
    assert CoolingAlert.POSSIBLE_CAVITATION in action.alerts


def test_gradual_flow_rate_decrease_warning(strategy):
    s = strategy
    # todo: modify to have flow rate measured over loong time
    #   and be immune to intentional changes of flow rate

    for flow in [1.0, 0.8, 0.6, 0.4]:  # gradually decreasing
        s.update_state(CoolingData(temps=[30], flow_rate=flow))
    action = s.get_action()
    assert CoolingAlert.FLOW_DEGRADATION in action.alerts


def test_high_temperature_delta_between_input_output(strategy):
    s = strategy
    s.update_state(CoolingData(temps=[30, 60], flow_rate=1))  # assuming first is input, second is output
    action = s.get_action()
    assert CoolingAlert.HIGH_TEMP_DELTA in action.alerts


def test_inconsistent_sensor_readings_alert(strategy):
    s = strategy
    s.update_state(CoolingData(temps=[30, 60, 25, 55], flow_rate=1))  # too much variance
    action = s.get_action()
    assert CoolingAlert.SENSOR_INCONSISTENCY in action.alerts


def test_rapid_temperature_increase_produces_alert(strategy):
    s = strategy
    s.update_state(CoolingData(temps=[30], flow_rate=1))
    s.update_state(CoolingData(temps=[50], flow_rate=1))  # 20C jump
    action = s.get_action()
    assert CoolingAlert.RAPID_TEMP_INCREASE in action.alerts

