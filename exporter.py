#!/usr/bin/env python
"""Exports environment data for Prometheus to scrape."""

import logging
from time import sleep

from bme280 import BME280
from prometheus_client import Gauge, start_http_server

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

logging.basicConfig(
    format="%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

POLLING_INTERVAL = 5  # seconds
# Tuning factor for compensation. Decrease this number to adjust the
# temperature down, and increase to adjust up
COMPENSATION_FACTOR = 2.25
EXPORTER_PORT = 9877


def get_cpu_temperature() -> float:
    with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
        temp = f.read()
        temp = int(temp) / 1000.0
    return temp


def compensate_raw_temperature(raw_temp: float) -> float:
    cpu_temp = get_cpu_temperature()
    comp_temp = raw_temp - ((cpu_temp - raw_temp) / COMPENSATION_FACTOR)
    return comp_temp


def main():
    bme280 = BME280(i2c_dev=SMBus(1))
    # initialize (first reading tends to be way off)
    bme280.get_temperature()
    sleep(1)

    temperature_gauge_raw = Gauge("environ_temp_raw", "Environment Temperature (raw)")
    temperature_gauge = Gauge("environ_temp", "Environment Temperature")
    # start http server, providing readings
    # logging.DEBUG(f"Starting HTTP Server at localhost:{EXPORTER_PORT}")
    start_http_server(EXPORTER_PORT)

    while True:
        temp_raw = bme280.get_temperature()
        # logging.DEBUG(f"{temp_raw=:.01f}")
        temp = compensate_raw_temperature(temp_raw)
        # logging.DEBUG(f"{temp=:.01f}")

        temperature_gauge_raw.set(temp_raw)
        temperature_gauge.set(temp)

        sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    main()
