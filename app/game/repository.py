import tortoise.exceptions

from app.common.exceptions.entity_exception import ResourceNotFound
from app.common.utils.types import MISSING
from app.game.entities import GameEntity


class GameRepository:
    @classmethod
    async def create(
        cls,
        name: str,
        description: str | None = None,
        theme: list | None = MISSING,
        min_player_count: int | None = 1,
        max_player_count: int | None = 2,
    ) -> GameEntity:
        if theme is MISSING:
            theme = []
        return await GameEntity.create(
            **{
                "name": name,
                "description": description,
                "theme": theme,
                "min_player_count": min_player_count,
                "max_player_count": max_player_count,
            }
        )

    @classmethod
    async def get_by_id(cls, game_id: str, /) -> GameEntity:
        try:
            if not await cls.exist(id=game_id):
                raise ResourceNotFound(resource_id=game_id)
            return await GameEntity.get(id=game_id)
        except tortoise.exceptions.OperationalError:
            raise ResourceNotFound(resource_id=game_id)

    @classmethod
    async def exist(cls, *args, **kwargs) -> bool:
        return await GameEntity.exists(*args, **kwargs)

    @classmethod
    async def list_all(cls) -> list[GameEntity]:
        return await GameEntity.all()

    @classmethod
    async def modify(cls, entity_id: str, **kwargs) -> GameEntity:
        try:
            if not await cls.exist(id=entity_id):
                raise ResourceNotFound(resource_id=entity_id)
            entity = await GameEntity.get(id=entity_id)
            await entity.delete()
        except tortoise.exceptions.OperationalError:
            raise ResourceNotFound(resource_id=entity_id)

        for key, value in kwargs.items():
            if value is not MISSING:
                setattr(entity, key, value)
        await entity.save()
        return entity

    @classmethod
    async def delete(cls, entity_id: str) -> None:
        try:
            if not await cls.exist(id=entity_id):
                raise ResourceNotFound(resource_id=entity_id)
            entity = await GameEntity.get(id=entity_id)
            await entity.delete()
        except tortoise.exceptions.OperationalError:
            raise ResourceNotFound(resource_id=entity_id)
