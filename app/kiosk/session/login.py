from aredis_om import JsonModel

__all__ = ["KioskLoginSession"]


class KioskLoginSession(JsonModel):
    name: str | None = None
    user_agent: str
    table_id: str | None = None
    is_authenticated: bool
    login_key: str | None = None
    # pk: SESSION_ID
