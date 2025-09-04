from datetime import datetime

from aredis_om import JsonModel, EmbeddedJsonModel


class SessionMember(EmbeddedJsonModel):
    user_id: str
    username: str
    joined_at: str  # ISO formatted datetime string


class SessionGame(EmbeddedJsonModel):
    gid: str
    name: str
    max_player_count: int
    current_players: int = 0


class SessionRoom(JsonModel):
    game: SessionGame
    kiosk_id: str | None = None
    members: list[SessionMember] = []
    created_at: datetime  # ISO formatted datetime string
    updated_at: datetime  # ISO formatted datetime string
