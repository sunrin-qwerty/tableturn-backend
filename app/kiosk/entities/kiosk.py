from tortoise import Model, fields

from app.common.entity_mixins import UUIDEntityMixin

__all__ = ["KioskAccountEntity"]


class KioskAccountEntity(Model, UUIDEntityMixin):
    name = fields.CharField(max_length=100)
    table_id = fields.CharField(max_length=2, unique=True)
    tokenw = fields.CharField(max_length=100)

    __repr__ = (
        lambda self: f"<KioskAccount id={self.id}, email={self.email}, is_active={self.is_active}>"
    )

    class Meta:
        table = "kiosk_accounts"
