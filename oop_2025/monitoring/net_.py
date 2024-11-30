import socket
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from time import sleep

from pydantic import BaseModel


def measure_latency(domain, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        start_time = time.time()
        sock.connect((domain, port))
        end_time = time.time()
        sock.close()
    except (OSError, socket.timeout):
        return -1
    return (end_time - start_time) * 1000  # Convert to milliseconds


class NetworkDevice(BaseModel):
    id: int
    ip: str
    port: int
    name: str = 'N/A'
    ip_resolved_at: datetime = None


class PingResult(BaseModel):
    device_id: int
    latency_ms: float
    sent_at: datetime


class PingResultStorage:
    def store(self, ping_result: PingResult):
        pass
    def get_results(self, device_id: int, since: datetime) -> list[PingResult]:
        pass

class MonitorInfo(BaseModel):
    ip: str
    name: str


class MonitorConfig(BaseModel):
    ping_dealy: float
    join_token: str


class MonitorEngine:
    def __init__(self, config: MonitorConfig):
        self.config = config
        self.is_running = False
        self.devices: dict[int, NetworkDevice] = {}
        self.executor: ThreadPoolExecutor = None

    def __periodic_job(self):
        while self.is_running:
            for device in self.devices.values():
                self.executor.submit(get_latency_ms, device)
            sleep(self.config.ping_dealy)

    def __check_device(self, device_id: int):
        device = self.devices.get(device_id)
        latency = get_latency_ms(device)


    def start(self):
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.is_running = True
        self.executor.submit(self.__periodic_job)

    def stop(self):
        self.executor.shutdown()
        # todo: cancel scheduled jobs
        self.is_running = False

    def add_device(self, device: NetworkDevice):
        self.devices[device.id] = device

    def remove_device(self, device_id: int):
        self.devices.pop(device_id)

    def get_results(self, device_ids: list[int], since: datetime) -> list[PingResult]:
        pass


def get_latency_ms(device: NetworkDevice) -> float:
    return measure_latency(device.ip, device.port)


def get_devices() -> list[NetworkDevice]:
    devices = []
    devices.append(NetworkDevice(ip='1.1.1.1', port=53))
    devices.append(NetworkDevice(ip='8.8.8.8', port=443))
    return devices


if __name__ == '__main__':
    devs = get_devices()
    while True:
        for d in devs:
            lat = get_latency_ms(d)
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print(f'{current_time}', f'{f"{d.ip}:{d.port}":<30}{lat:.2f} ms')
        time.sleep(2)
