from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class Habit:
    name: str
    frequency: str  # "daily", "weekly", "monthly"
    created: str = datetime.now().isoformat()  # ISO timestamp
    completions: List[str] = None
    reminder_time: Optional[str] = None  # "HH:MM" format only

    def __post_init__(self):
        self.completions = self.completions or []