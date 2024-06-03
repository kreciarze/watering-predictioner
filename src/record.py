from typing import Annotated

from pandas import DataFrame
from pydantic import BaseModel


class Record(BaseModel):
    soil_moisture: Annotated[int, "in %, usually between 1 and 90"]
    temperature: Annotated[int, "in Celsius, usually between 0 and 45"]
    time: Annotated[int, "usually between 0 and 110"]
    air_temperature: Annotated[float, "in Celsius, usually between 11.20 and 45.56"]
    air_humidity: Annotated[float, "in %, usually between 0.59 and 96.00"]
    pressure: Annotated[float, "KPa, usually between 100.50 and 101.86"]

    def to_df(self) -> DataFrame:
        return DataFrame([self.model_dump()])

    def to_row(self) -> list[str]:
        attrs = [
            self.soil_moisture,
            self.temperature,
            self.time,
            self.air_temperature,
            self.air_humidity,
            self.pressure,
        ]
        return list(map(str, attrs))
