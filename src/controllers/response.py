from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Response:
    status_code: int
    body: Dict[str, Any]
