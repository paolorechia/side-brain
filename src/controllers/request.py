from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional


class HTTPMethod(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass(frozen=True)
class Request:
    resource: str
    method: HTTPMethod
    path_parameters: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None

    def get_body_prop(self, prop: str) -> Any:
        if self.body:
            return self.body[prop]
        return None
