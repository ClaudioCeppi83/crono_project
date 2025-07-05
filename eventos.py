from enum import Enum, auto
from typing import List, Optional

class EventMode(Enum):
    INFINITE = auto()
    PREDEFINED = auto()
    MAXIMUM = auto()

class EventManager:
    """Gestiona la configuración y lógica de los modos de evento para el cronómetro."""
    def __init__(self):
        self.mode: Optional[EventMode] = None
        self.lap_names: List[str] = []
        self.max_laps: Optional[int] = None
        self.next_lap_index: int = 0

    def configure_session(self, mode: EventMode, lap_names: Optional[List[str]] = None, max_laps: Optional[int] = None):
        self.mode = mode
        self.lap_names = lap_names if lap_names is not None else []
        self.max_laps = max_laps
        self.next_lap_index = 0

    def get_next_lap_name(self) -> str:
        if self.mode == EventMode.PREDEFINED and self.lap_names:
            if self.next_lap_index < len(self.lap_names):
                name = self.lap_names[self.next_lap_index]
            else:
                name = f"Lap {self.next_lap_index + 1}"
        elif self.mode == EventMode.MAXIMUM:
            name = f"Lap {self.next_lap_index + 1}"
        else:
            name = f"Lap {self.next_lap_index + 1}"
        return name

    def can_record_lap(self) -> bool:
        if self.mode == EventMode.PREDEFINED and self.lap_names:
            return self.next_lap_index < len(self.lap_names)
        elif self.mode == EventMode.MAXIMUM and self.max_laps is not None:
            return self.next_lap_index < self.max_laps
        return True

    def advance_lap(self):
        self.next_lap_index += 1
