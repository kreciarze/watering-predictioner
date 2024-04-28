import time
import Adafruit_ADS1x15
from bmp280 import BMP280

from helper import (
    convert_soil_moisture_to_dataset_range,
    convert_luminescence_to_dataset_range,
)
from record import Record


class Measurer:
    adc = None
    bus = None
    bmp280 = None
    moisture_col_name = "moisture"
    luminescence_col_name = "luminescence"
    MOIST_GAIN = 2 / 3
    GAIN = 1

    def __init__(self):
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48, busnum=1)
        try:
            from smbus2 import SMBus
        except ImportError:
            from smbus import SMBus

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

    def read_from_sensors(self, measure_luminescence: bool = False) -> Record:
        reading = Record()
        ## Measure Moisture
        self.adc.start_adc(0, gain=self.MOIST_GAIN)
        conv_reading = convert_soil_moisture_to_dataset_range(
            self.adc.get_last_result()
        )
        reading.soil_moisture = conv_reading
        time.sleep(0.2)

        ## Measure Luminescence
        if measure_luminescence:
            self.adc.start_adc(1, gain=self.GAIN)
            conv_reading = convert_luminescence_to_dataset_range(
                self.adc.get_last_result()
            )
            reading[self.luminescence_col_name] = conv_reading

        ## Measure Temperature and Pressure
        air_temperature = self.bmp280.get_temperature()
        reading.air_temperature = air_temperature

        pressure = self.bmp280.get_pressure()
        reading.pressure = pressure
        ## Still missing some sensors, for now just return const values
        reading.time = 10
        reading.temperature = 30.5
        reading.air_humidity = 70.5

        return reading


def measure_conditions() -> Record:
    return Record(
        soil_moisture=50,
        temperature=30,
        time=10,
        air_temperature=30.5,
        air_humidity=70.5,
        pressure=100.5,
    )
