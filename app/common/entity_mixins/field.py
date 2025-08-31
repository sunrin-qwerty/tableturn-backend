from tortoise.fields import Field


__all__ = ["S3ContentField", "S3File"]


class S3File:
    def __init__(self, id_, path_):
        self.id = id_
        self.path = path_

    @property
    def url(self):
        return f"https://s3.amazonaws.com/{self.path}"


class S3ContentField(Field):
    SQL_TYPE = "VARCHAR(255)"

    def to_db_value(self, value, instance):
        if isinstance(value, S3File):
            return f"{value.id}|{value.path}"
        return value

    def to_python_value(self, value):
        if isinstance(value, S3File):
            return value
        if value:
            id_, path_ = value.split("|", 1)
            return S3File(id_, path_)
        return None
