import csv
import os
import time

import Adafruit_ADS1x15
import adafruit_dht
import board
from bmp280 import BMP280

from record import Record

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus  # type: ignore[no-redef]


class Measurer:
    OLD_HUMIDITY = 25
    MOISTURE_COL_NAME = "moisture"
    LUMINESCENCE_COL_NAME = "luminescence"
    CSV_PATH = "data/logs/record.csv"
    MOIST_GAIN = 2 / 3
    GAIN = 1

    def __init__(self, csv_path: str = "") -> None:
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        self.dht_device = adafruit_dht.DHT11(board.D4)
        self.csv_path = csv_path or self.CSV_PATH
        self.csv_path = os.path.join(os.path.dirname(__file__), self.csv_path)
        self.bus = SMBus(1)
        self.bmp280 = BMP280(i2c_dev=self.bus)

    def save_to_csv(self, record: Record) -> None:
        with open(self.csv_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(record.to_row())

    def read_from_sensors(self) -> tuple[Record, float]:
        soil_moisture_reading = self.measure_soil_moisture()
        time.sleep(0.2)

        record = Record(
            soil_moisture=int(soil_moisture_reading),
            temperature=self.bmp280.get_temperature(),
            time=55,
            air_temperature=self.bmp280.get_temperature(),
            air_humidity=self.measure_humidity(),
            pressure=self.bmp280.get_pressure(),
        )

        self.save_to_csv(record)
        return record, self.measure_luminescence()

    def measure_soil_moisture(self) -> float:
        self.adc.start_adc(0, gain=self.MOIST_GAIN)
        soil_moisture_reading = self.convert_soil_moisture_to_dataset_range(self.adc.get_last_result())
        return soil_moisture_reading

    def measure_humidity(self) -> float:
        try:
            humidity = self.dht_device.humidity
            self.OLD_HUMIDITY = humidity
            return humidity
        except RuntimeError:
            return self.OLD_HUMIDITY

    def measure_luminescence(self) -> float:
        self.adc.start_adc(1, gain=self.GAIN)
        luminescence_value = self.convert_luminescence_to_dataset_range(self.adc.get_last_result())
        return luminescence_value

    @staticmethod
    def convert_soil_moisture_to_dataset_range(value: float) -> float:
        if value >= 19200:
            return 90.0
        elif value <= 8864:
            return 0.0
        else:
            return (value - 8864) / (19200 - 8864) * 90.0

    @staticmethod
    def convert_luminescence_to_dataset_range(value: float) -> float:
        if value >= 24000:
            return 100.0
        elif value <= 100:
            return 0.0
        else:
            return (value - 100) / (24000 - 100) * 100.0
