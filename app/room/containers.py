from dependency_injector import containers, providers

from app.room.repository import RoomRepository
from app.room.services import RoomService


class RoomContainer(containers.DeclarativeContainer):
    repository: RoomRepository = providers.Singleton(RoomRepository)
    service: RoomService = providers.Factory(
        RoomService,
        room_repository=repository,
    )
