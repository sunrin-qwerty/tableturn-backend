from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.postgres.fields import ArrayField

from app.common.entity_mixins import UUIDEntityMixin

__all__ = ["GameEntity"]


class GameEntity(Model, UUIDEntityMixin):
    name = fields.CharField(max_length=100)
    description = fields.TextField(null=True)
    theme = ArrayField(element_type="text", null=True)
    min_player_count = fields.IntField(default=1)
    max_player_count = fields.IntField(default=1)

    __repr__ = (
        lambda self: f"<Game id={self.id}, name={self.name} player={self.min_player_count}~{self.max_player_count}>"
    )

    class Meta:
        table = "games"
