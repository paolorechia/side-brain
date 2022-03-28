from typing import Union

from src.domain import commands
from src.service.collection_service import CollectionService

from .response import Response


def get_router():
    pass


def invoke(
    command: Union[
        commands.CreateCollectionCommand,
        commands.RenameCollectionCommand,
        commands.GetAllCollectionsCommand,
        commands.AddItemToCollectionCommand,
        commands.DeleteCollectionCommand,
        commands.UpdateItemCommand,
        commands.GetCollectionStatisticsCommand,
        commands.GetNextCollectionItemCommand,
        commands.SuggestCommand,
    ],
    service: CollectionService,
) -> Response:
    if isinstance(command, commands.CreateCollectionCommand):
        new_collection = service.create_collection(command.name)
        # new_collection["collection"] = new_collection["collection"]["uuid"]
        return Response(201, new_collection)

    elif isinstance(command, commands.RenameCollectionCommand):
        new_collection = service.rename_collection(command.uuid, command.name)
        # new_collection["collection"] = new_collection["collection"]["uuid"]
        return Response(200, new_collection)

    elif isinstance(command, commands.GetAllCollectionsCommand):
        collections = service.get_collections()
        return Response(200, collections)

    elif isinstance(command, commands.AddItemToCollectionCommand):
        service.add_item_to_collection(
            command.item_type, command.hint, command.answer, command.collection_uuid
        )
        return Response(200, {})

    elif isinstance(command, commands.UpdateItemCommand):
        service.update_item(
            command.item_uuid, command.item_type, command.hint, command.answer
        )
        return Response(200, {})

    elif isinstance(command, commands.DeleteCollectionCommand):
        service.delete_collection(command.collection_uuid)
        return Response(200, {})

    elif isinstance(command, commands.SuggestCommand):
        suggestions = service.suggest()
        return Response(200, suggestions)

    else:
        return Response(400, {"error": "Invalid Command: {}".format(command)})
