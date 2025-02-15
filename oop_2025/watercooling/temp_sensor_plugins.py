from loguru import logger

from oop_2025.watercooling.sensors import Sensor, ThermalSensor


class CPULinuxTemperatureSensor(ThermalSensor):

    def get_temperatures(self) -> list[float]:
        pass

    def parse_output(self, lines: list[str]) -> list[float]:
        pass


class RefLinuxTemperatureSensor(CPULinuxTemperatureSensor):
    def __init__(self):
        self.temps = []

    def get_temperatures(self) -> list[float]:
        # launch `sensors` command, and parse it with self.parse_output
        return self.temps

    def parse_output(self, lines: list[str]) -> set[float]:
        cpu_manufacturer = None
        temps = []
        for ln in lines:
            ln = ln.strip()
            if not cpu_manufacturer:
                if 'coretemp-isa' in ln:
                    cpu_manufacturer = 'intel'
                if 'k10temp-pci' in ln:
                    cpu_manufacturer = 'amd'
                continue
            else:
                # logger.debug(f'[{ln}')
                if len(ln) == 0:
                    break
                if '°C' in ln:
                    ln = ln.split('°C')[0].split(':')[1].strip()
                    temps.append(float(ln))
        return set(temps)


def load_file(file_name: str) -> list[str]:
    with open(file_name, encoding='utf-8') as f:
        lines = f.readlines()
        return lines


def test_amd1():
    cpu_sensor = RefLinuxTemperatureSensor()
    read = cpu_sensor.parse_output(load_file("experimental/example1_amd.txt"))

    answer = set(read)

    expected = {53.0, 37.8, 38.4, 36.9, 37.1, 37.5, 37.0, 37.6, 36.4}

    assert answer == expected


def test_amd2():
    cpu_sensor = RefLinuxTemperatureSensor()
    read = cpu_sensor.parse_output(load_file("experimental/example3_amd.txt"))

    answer = set(read)
    expected = {53.2}

    assert answer == expected


def test_intel1():
    cpu_sensor = RefLinuxTemperatureSensor()
    read = cpu_sensor.parse_output(load_file("experimental/example2_intel.txt"))

    answer = set(read)
    expected = {29.0, 30.0, 28.0}

    """
    note -- other lines from the output of `sensor` command correspond to different hardware (not CPU)
    """

    assert answer == expected


def test_intel2():
    cpu_sensor = RefLinuxTemperatureSensor()
    read = cpu_sensor.parse_output(load_file("experimental/example4_intel.txt"))

    answer = set(read)
    expected = {38.0, 37.0}

    """
    note -- other lines from the output of `sensor` command correspond to different hardware (not CPU)
    """

    assert answer == expected


def test_intel3():
    cpu_sensor = RefLinuxTemperatureSensor()
    read = cpu_sensor.parse_output(load_file("experimental/example5_intel.txt"))

    answer = set(read)
    expected = {52.0, 49.0, 48.0}

    """
    note -- other lines from the output of `sensor` command correspond to different hardware (not CPU)
    """

    assert answer == expected
