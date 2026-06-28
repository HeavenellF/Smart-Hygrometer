from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Event(Enum):
    WINDOW_OPEN = "window_open"
    WINDOW_CLOSE = "window_close"
    DOOR_OPEN = "door_open"
    DOOR_CLOSE = "door_close"
    DRY_CLEANING = "dry_cleaning"
    WATER_BOWL = "water_bowl"


@dataclass
class HygrometerReading:
    timestamp: datetime
    temperature: float
    humidity: float
    events: list[Event] = field(default_factory=list)

    def add_event(self, event: Event) -> None:
        if event not in self.events:
            self.events.append(event)

    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "temperature": self.temperature,
            "humidity": self.humidity,
            "events": [e.value for e in self.events],
        }