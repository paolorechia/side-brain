from src.domain import commands
from src.service.collection_service import CollectionService

from .response import Response


def get_router():
    pass


def invoke(
    command: commands.CreateCollectionCommand, service: CollectionService
) -> Response:
    if isinstance(command, commands.CreateCollectionCommand):
        new_collection = service.create_collection(command.name)
        new_collection["collection"] = new_collection["collection"]["uuid"]
        return Response(200, new_collection)

    else:
        return Response(400, {"Invalid Command: %s", command})
