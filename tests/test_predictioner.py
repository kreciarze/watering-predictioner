from predictioner import Record, should_water_plant


def test_watering_prediction() -> None:
    record = Record(
        soil_moisture=50,
        temperature=30,
        time=10,
        air_temperature=30.5,
        air_humidity=70.5,
        pressure=100.5,
    )
    should_water = should_water_plant(record=record)
    assert type(should_water) is bool
