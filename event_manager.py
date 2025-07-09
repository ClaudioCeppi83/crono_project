from enum import Enum, auto
from typing import List, Optional, Tuple

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
        self.laps: List[Tuple[str, str]] = []

    def configure_session(self, mode: EventMode, lap_names: Optional[List[str]] = None, max_laps: Optional[int] = None):
        self.mode = mode
        self.lap_names = lap_names if lap_names is not None else []
        self.max_laps = max_laps
        self.next_lap_index = 0

    def get_next_lap_name(self) -> str:
        if self.mode == EventMode.PREDEFINED and self.next_lap_index < len(self.lap_names):
            return self.lap_names[self.next_lap_index]
        return f"Lap {self.next_lap_index + 1}"

    def can_record_lap(self) -> bool:
        if self.mode == EventMode.PREDEFINED:
            return self.next_lap_index < len(self.lap_names)
        if self.mode == EventMode.MAXIMUM:
            return self.max_laps is None or self.next_lap_index < self.max_laps
        return True

    def record_lap(self, lap_time: str):
        lap_name = self.get_next_lap_name()
        self.laps.append((lap_name, lap_time))
        self.next_lap_index += 1

    def get_laps(self) -> List[Tuple[str, str]]:
        return self.laps

    def reset_laps(self):
        self.laps = []
        self.next_lap_index = 0

    def get_mode_name(self) -> str:
        return self.mode.name if self.mode else "INFINITE"
