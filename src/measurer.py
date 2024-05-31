import time
import csv
import os

import board
import Adafruit_ADS1x15
import adafruit_dht
from bmp280 import BMP280

from helper import (
    convert_soil_moisture_to_dataset_range,
    convert_luminescence_to_dataset_range,
)
from record import Record
from datetime import datetime
from config import RECORD_DIR

def measure_conditions(test = False) -> Record:
    # TODO:
    # 1. Get data new data reading
    # 2. Return a Record object with the data
    if test:
        return Record(
            soil_moisture=10,
            temperature=20,
            time=10,
            air_temperature=20,
            air_humidity=20,
            pressure=20,
        )

class Measurer:
    adc = None
    bus = None
    bmp280 = None
    dht_device = None
    old_humidity = 25
    moisture_col_name = "moisture"
    luminescence_col_name = "luminescence"
    csv_path = "data/logs/record.csv"
    MOIST_GAIN = 2 / 3
    GAIN = 1

    def __init__(self, csv_path=""):
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        self.dht_device = adafruit_dht.DHT11(board.D4)
        try:
            from smbus2 import SMBus
        except ImportError:
            from smbus import SMBus

        if csv_path != "":
            self.csv_path = csv_path
        self.csv_path = os.path.join(os.path.dirname(__file__), self.csv_path)

        self.bus = SMBus(1)
        self.bmp280 = BMP280(i2c_dev=self.bus)

    def mock_measure_conditions(self) -> Record:
        return Record(
            soil_moisture=50,
            temperature=30,
            time=10,
            air_temperature=30.5,
            air_humidity=70.5,
            pressure=100.5,
        )

    def save_to_csv(self, record: Record) -> None:
        with open(self.csv_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(record.csv_str().split(","))

    def read_from_sensors(
        self,
    ) -> (Record, float):
        ## Measure Moisture
        self.adc.start_adc(0, gain=self.MOIST_GAIN)
        soil_moisture_reading = convert_soil_moisture_to_dataset_range(self.adc.get_last_result())
        time.sleep(0.2)

        ## Measure Luminescence
        self.adc.start_adc(1, gain=self.GAIN)
        luminescence_value = convert_luminescence_to_dataset_range(self.adc.get_last_result())

        ## Measure Temperature and Pressure
        air_temperature = self.bmp280.get_temperature()
        pressure = self.bmp280.get_pressure()

        ## Measure Humidity
        try:
            humidity = self.dht_device.humidity
            self.old_humidity = humidity
        except RuntimeError as _:
            humidity = self.old_humidity

        return (
            Record(
                soil_moisture=int(soil_moisture_reading),
                temperature=30,
                time=55,
                air_temperature=air_temperature,
                air_humidity=humidity,
                pressure=pressure,
            ),
            luminescence_value,
        )


def measure_conditions() -> Record:
    return Record(
        soil_moisture=50,
        temperature=30,
        time=10,
        air_temperature=30.5,
        air_humidity=70.5,
        pressure=100.5,
    )

    today = datetime.today().strftime('%Y_%m_%d')
    log_dir = f"{RECORD_DIR}-{today}.csv"
    with open(log_dir, "r") as f:
        lines = f.readlines()
        if len(lines) < 10:
            return Record(
                soil_moisture=0,
                temperature=0,
                time=0,
                air_temperature=0,
                air_humidity=0,
                pressure=0,
            )

        last_ten_lines = lines[-10:]
        avg_measure = [0, 0, 0, 0, 0, 0]
        for line in last_ten_lines:
            data = line.split(",")
            for i in range(6):
                avg_measure[i] += float(data[i])
        for i in range(6):
            avg_measure[i] /= 10

        return Record(
            soil_moisture=int(avg_measure[0]),
            temperature=avg_measure[1],
            time=avg_measure[2],
            air_temperature=avg_measure[3],
            air_humidity=avg_measure[4],
            pressure=avg_measure[5],
        )

