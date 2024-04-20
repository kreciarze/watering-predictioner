from time import sleep

from controller import water_plant
from measurer import measure_conditions
from predictioner import decide_whether_to_water


def main() -> None:
    interval = 60 * 60 * 2  # 2 hours
    while True:
        record = measure_conditions()
        should_water = decide_whether_to_water(record=record)

        if should_water:
            water_plant()
        else:
            print("Not watering the plant")  # noqa: T201

        sleep(interval)


if __name__ == "__main__":
    main()
