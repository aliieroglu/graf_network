from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Node:
    id: str
    label: Optional[str] = None
    activity: Optional[float] = None
    interaction: Optional[float] = None
    connection_count: Optional[int] = None
