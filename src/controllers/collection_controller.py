from typing import Dict, Any
from src.service.collection_service import CollectionService
from .response import Response

def create_collection(request: Dict[str, Any], service: CollectionService) -> Response:
    name = request["name"]
    new_collection = service.create_collection(name)
    new_collection["collection"] = new_collection["collection"].to_dict()
    return Response(
        200,
        new_collection
    )

