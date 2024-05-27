from time import sleep

from gpiozero import LED
from controller import water_plant
from measurer import measure_conditions, Measurer
from predictioner import decide_whether_to_water
import csv


def main() -> None:
    interval = 1  # 60 * 60 * 2  # 2 hours
    measurer = Measurer()
    led_blue = LED(17)
    led_red = LED(27)

    while True:
        record = measurer.read_from_sensors(True)
        # Save record value to CSV file
        # measurer.save_to_csv(record)
        print(record)
        should_water = decide_whether_to_water(record=record)

        if should_water:
            water_plant()
            led_red.off()
            led_blue.on()
        else:
            print("Not watering the plant")  # noqa: T201
            led_blue.off()
            led_red.on()
        sleep(interval)


if __name__ == "__main__":
    main()
