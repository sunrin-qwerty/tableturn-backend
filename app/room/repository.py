from app.kiosk.entities import KioskAccountEntity
from app.room.session import SessionRoom, SessionGame, SessionMember

from app.common.utils.generate import generate_uuid

from app.common.types import ROOM_ID
from datetime import datetime


class RoomRepository:
    @classmethod
    async def create(cls, kiosk_id: str) -> ROOM_ID:
        ready_fake_game = SessionGame(
            gid="lobby", name="Lobby", max_player_count=4, current_players=0
        )
        room_session = SessionRoom(
            kiosk_id=kiosk_id,
            game=ready_fake_game,
            members=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        await room_session.save()
        return room_session.pk

    @classmethod
    async def close(cls, room_id: str) -> None:
        room = await SessionRoom.get(room_id)
        if room:
            await room.delete(pk=room_id)

    @classmethod
    async def get(cls, room_id: str) -> SessionRoom | None:
        room = await SessionRoom.get(room_id)
        return room
