from pydantic import BaseModel, Field
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(gt=0, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime = Field(le=datetime(2026, 1, 1))
    is_operational: bool = Field(default=True)
    notes: str = Field(default=None, max_length=200)


if __name__ == "__main__":
    print("Space Station Data Validation\n"
          "========================================")
    try:
        space_station = SpaceStation(station_id="ISS001",
                                     name="International Space Station",
                                     crew_size="6",
                                     power_level="85.5",
                                     oxygen_level="92.3",
                                     last_maintenance="2023-12-05")
        print("Valid station created:")
        print("ID: ", space_station.station_id)
        print("Name:", space_station.name)
        print("Crew", space_station.crew_size, "people")
        print("Power:", space_station.power_level, "%")
        print("Oxygen", space_station.oxygen_level, "%")
        if space_station.is_operational:
            print("Status: Operational")
        else:
            print("Status: Not Operational")
    except Exception as e:
        print("=====================================")
        print(f"Expected validation error:\n {e}")
    try:
        space_station = SpaceStation(station_id="ISS001",
                                     name="International Space Station",
                                     crew_size="27",
                                     power_level="85.5",
                                     oxygen_level="92.3",
                                     last_maintenance="2023-12-05")
        print("Valid station created:")
        print("ID: ", space_station.station_id)
        print("Name:", space_station.name)
        print("Crew", space_station.crew_size, "people")
        print("Power:", space_station.power_level, "%")
        print("Oxygen", space_station.oxygen_level, "%")
        if space_station.is_operational:
            print("Status: Operational")
        else:
            print("Status: Not Operational")
    except Exception as e:
        print("=====================================")
        print(f"Expected validation error:\n {e.errors()[0]['msg']}")
