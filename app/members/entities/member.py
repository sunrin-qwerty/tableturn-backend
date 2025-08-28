from tortoise import Model, fields

from app.common.entity_mixins import UUIDEntityMixin

__all__ = ["MemberEntity"]


class MemberEntity(Model, UUIDEntityMixin):
    nickname = fields.CharField(max_length=100)
    email = fields.CharField(max_length=100)
    profile_url = fields.CharField(max_length=255, null=True)
    is_admin = fields.BooleanField(default=False)

    __repr__ = (
        lambda self: f"<Member id={self.id}, nickname={self.username}, email={self.email}>"
    )

    class Meta:
        table = "members"
