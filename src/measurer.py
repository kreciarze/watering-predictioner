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