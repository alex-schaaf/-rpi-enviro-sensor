# rpi-enviro-sensor

Software to read out sensor data from a Enviro(+) sensor hat on a Raspberry Pi Zero WH and serving readings for [Prometheus](https://prometheus.io/).

## Installation

Installation is best done using the official one-liner provided by [pimoroni](https://github.com/pimoroni/enviroplus-python):

```
curl -sSL https://get.pimoroni.com/enviroplus | bash
```

Then install the Python client for Prometheus:

```
pip install prometheus-client
```

## Run

```
nohup ./exporter.py &
```

To find the process use `ps ax | grep exporter.py `to get the process ID. To stop the execution run `kill <process id>`
