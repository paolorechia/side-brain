from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class Response:
    status_code: int
    body: Dict[str, Any]