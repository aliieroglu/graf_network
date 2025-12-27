from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Node:
    id: str
    label: Optional[str] = None
