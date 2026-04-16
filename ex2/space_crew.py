from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime = Field(...)
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_mission(self):
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        has_leader = False
        for member in self.crew:
            if member.rank in [Rank.commander, Rank.captain]:
                has_leader = True
            if not member.is_active:
                raise ValueError("All crew members must be active")
        if not has_leader:
            raise ValueError("Mission must have at least one Commander or Captain")
        if self.duration_days > 365:
            experienced = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    experienced += 1
            if experienced < len(self.crew) / 2:
                raise ValueError("Long missions need at least 50% experienced crew")
        return self


if __name__ == "__main__":
    print("Space Mission Crew Validation\n"
          "=========================================")
    try:
        mission = SpaceMission(mission_id="M2024_MARS",
                               mission_name="Mars Colony Establishment",
                               destination="Mars",
                               launch_date="2024-06-01T10:00:00",
                               duration_days="900",
                               budget_millions="2500.0",
                               crew=[
                                   {
                                       "member_id": "C01",
                                       "name": "Sarah Connor",
                                       "rank": "commander",
                                       "age": 40,
                                       "specialization": "Mission Command",
                                       "years_experience": 10
                                   },
                                   {
                                       "member_id": "C02",
                                       "name": "John Smith",
                                       "rank": "lieutenant",
                                       "age": 35,
                                       "specialization": "Navigation",
                                       "years_experience": 6
                                   },
                                   {
                                       "member_id": "C03",
                                       "name": "Alice Johnson",
                                       "rank": "officer",
                                       "age": 30,
                                       "specialization": "Engineering",
                                       "years_experience": 5
                                   }
                               ])
        print("Valid mission created:")
        print("Mission:", mission.mission_name)
        print("ID:", mission.mission_id)
        print("Destination:", mission.destination)
        print("Duration:", mission.duration_days, "days")
        print("Budget: $", mission.budget_millions, "M")
        print("Crew size:", len(mission.crew))
        print("Crew members:")
        for member in mission.crew:
            print("-", member.name, "(", member.rank, ")-", member.specialization)
    except Exception as e:
        print("=========================================")
        print(f"Expected validation error:\n {e}")

    try:
        mission = SpaceMission(mission_id="M2024_FAIL",
                               mission_name="Test Mission",
                               destination="Moon",
                               launch_date="2024-06-01T10:00:00",
                               duration_days="100",
                               budget_millions="500.0",
                               crew=[
                                   {
                                       "member_id": "C01",
                                       "name": "Bob",
                                       "rank": "officer",
                                       "age": 25,
                                       "specialization": "Science",
                                       "years_experience": 2
                                   }
                               ])
        print("Valid mission created:")
        print("Mission:", mission.mission_name)
    except Exception as e:
        print("=========================================")
        print(f"Expected validation error:\n {e.errors()[0]['msg']}")
