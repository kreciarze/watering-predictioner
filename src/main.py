from time import sleep

from controller import log_response
from measurer import measure_conditions
from predictioner import decide_whether_to_water


def main() -> None:
    interval = 10  # 10 seconds
    while True:
        record = measure_conditions()
        should_water = decide_whether_to_water(record=record)

        print(f"Should water: {should_water}")

        log_response(should_water)

        # Sleep for 2 hours
        sleep(interval)

if __name__ == "__main__":
    main()
