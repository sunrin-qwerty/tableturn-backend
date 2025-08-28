from aredis_om import JsonModel, EmbeddedJsonModel


class SessionMember(EmbeddedJsonModel):
    user_id: str
    username: str
    joined_at: str  # ISO formatted datetime string


class SessionGame(EmbeddedJsonModel):
    game_id: str
    game_name: str
    max_players: int
    current_players: int = 0


class SessionRoom(JsonModel):
    room_id: str
    game: SessionGame
    members: list[SessionMember] = []
    created_at: str  # ISO formatted datetime string
    updated_at: str  # ISO formatted datetime string
