from oop_2025.watercooling.sensors import Sensor, ThermalSensor


class CPULinuxTemperatureSensor(ThermalSensor):

    def get_temperatures(self) -> list[float]:
        pass

    def parse_output(self, lines: list[str]) -> list[float]:
        pass


def load_file(file_name: str) -> list[str]:
    with open(file_name) as f:
        lines = f.readlines()
        return lines


def test_amd1():
    cpu_sensor = CPULinuxTemperatureSensor()
    read = cpu_sensor.parse_output(load_file("experimental/example1_amd.txt"))

    answer = set(read)

    expected = {53.0, 37.8, 38.4, 36.9, 37.1, 37.5, 37.0, 37.6, 36.4}

    assert answer == expected


def test_amd2():
    cpu_sensor = CPULinuxTemperatureSensor()
    read = cpu_sensor.parse_output(load_file("experimental/example3_amd.txt"))

    answer = set(read)
    expected = {53.2}

    assert answer == expected


def test_intel1():
    cpu_sensor = CPULinuxTemperatureSensor()
    read = cpu_sensor.parse_output(load_file("experimental/example2_intel.txt"))

    answer = set(read)
    expected = {29.0, 30.0, 28.0}

    """
    note -- other lines from the output of `sensor` command correspond to different hardware (not CPU)
    """

    assert answer == expected
