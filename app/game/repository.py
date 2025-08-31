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
        return await GameEntity.get(id=game_id)

    @classmethod
    async def exist(cls, *args, **kwargs) -> bool:
        return await GameEntity.exists(*args, **kwargs)

    @classmethod
    async def list_all(cls) -> list[GameEntity]:
        return await GameEntity.all()

    @classmethod
    async def modify(cls, entity_id: str, **kwargs) -> GameEntity:
        entity = await GameEntity.get(id=entity_id)
        for key, value in kwargs.items():
            if value is not MISSING:
                setattr(entity, key, value)
        await entity.save()
        return entity

    @classmethod
    async def delete(cls, entity_id: str) -> None:
        entity = await GameEntity.get(id=entity_id)
        await entity.delete()
