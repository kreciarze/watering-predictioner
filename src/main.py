from datetime import datetime
from time import sleep

from gpiozero import LED

from config import SAVE_LOG_DIR
from measurer import Measurer
from predictioner import decide_whether_to_water


def main() -> None:
    interval = 1  # in seconds

    measurer = Measurer()
    led_blue = LED(17)
    led_red = LED(27)
    led_yellow = LED(22)

    while True:
        record, luminescence = measurer.read_from_sensors()

        print(record, luminescence)  # noqa: T201
        should_water = decide_whether_to_water(record=record)

        if luminescence < 1:
            led_yellow.on()
        else:
            led_yellow.off()

        if should_water:
            led_red.off()
            led_blue.on()
        else:
            led_blue.off()
            led_red.on()

        print(f"Should water: {should_water}")  # noqa: T201
        with open(f"{SAVE_LOG_DIR}/log_{datetime.today().strftime("%Y_%m_%d")}.csv", "a") as f:
            f.write(f"{datetime.now()},{should_water}\n")

        sleep(interval)


if __name__ == "__main__":
    main()
