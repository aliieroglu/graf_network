from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass(frozen=True)
class Edge:
    source_id: str
    target_id: str
    relation_type: Optional[str] = None
    relation_degree: Optional[float] = None

    def key(self) -> Tuple[str, str]:
        return tuple(sorted((self.source_id, self.target_id)))
