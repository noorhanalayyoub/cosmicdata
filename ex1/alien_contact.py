from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from enum import Enum


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime = Filed(default_factory=datetime.now)
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False) 
    
    @model_validator(mode="after")
    def check_rules(self):
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC'")

        if self.contact_type == ContactType.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")

        if self.contact_type == ContactType.telepathic and self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3 witnesses")

        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals should include received messages")
        return self


if __name__ == "__main__":
    print("Alien Contact Log Validation\n"
          "======================================")
    try:
        contact = AlienContact(contact_id="AC_2024_001",
                               timestamp="2024-05-01T12:00:00",
                               location="Area 51, Nevada",
                               contact_type="radio",
                               signal_strength="8.5",
                               duration_minutes="45",
                               witness_count="5",
                               message_received="Greetings from Zeta Reticuli")
        print("Valid contact report:")
        print("ID:", contact.contact_id)
        print("Type:", contact.contact_type)
        print("Location:", contact.location)
        print("Signal:", contact.signal_strength, "/10")
        print("Duration:", contact.duration_minutes, "minutes")
        print("Witnesses:", contact.witness_count)
        print("Message:", contact.message_received)
    except Exception as e:
        print("======================================")
        print(f"Expected validation error:\n {e}")
    try:
        contact = AlienContact(contact_id="AC_2024_002",
                               timestamp="2024-05-01T12:00:00",
                               location="Unknown",
                               contact_type="telepathic",
                               signal_strength="5.0",
                               duration_minutes="30",
                               witness_count="1")
        print("Valid contact report:")
        print("ID:", contact.contact_id)
    except Exception as e:
        print("======================================")
        print(f"Expected validation error:\n {e.errors()[0]['msg']}")
