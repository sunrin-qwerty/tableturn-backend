from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.postgres.fields import ArrayField

from app.common.entity_mixins import UUIDEntityMixin
from tortoise.contrib.pydantic import pydantic_model_creator


__all__ = ["GameEntity", "GameEntity_Pydantic", "GameEntityCreate_Pydantic"]


class GameEntity(Model, UUIDEntityMixin):
    name = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    image_path = fields.CharField(max_length=100, null=True)
    theme = ArrayField(element_type="text", null=True)
    min_player_count = fields.IntField(default=1)
    max_player_count = fields.IntField(default=1)

    __repr__ = (
        lambda self: f"<Game id={self.id}, name={self.name} player={self.min_player_count}~{self.max_player_count}>"
    )

    class Meta:
        table = "games"


GameEntity_Pydantic = pydantic_model_creator(GameEntity, name="GameEntity")
GameEntityCreate_Pydantic = pydantic_model_creator(
    GameEntity,
    name="GameEntityCreate",
    exclude_readonly=True,
    exclude=("id", "image_path"),
)
