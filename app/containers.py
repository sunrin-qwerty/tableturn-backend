from dependency_injector import containers, providers

from app.game.containers import GameContainer
from app.google.containers import GoogleContainer
from app.hello.containers import HelloContainer
from app.auth.containers import AuthContainer
from app.kiosk.containers import KioskContainer
from app.members.containers import MemberContainer


class AppContainers(containers.DeclarativeContainer):
    hello: HelloContainer = providers.Container(HelloContainer)
    google: GoogleContainer = providers.Container(GoogleContainer)
    member: MemberContainer = providers.Container(MemberContainer)
    auth: AuthContainer = providers.Container(
        AuthContainer,
        google_service=google.service,
        member_repository=member.repository,
    )
    kiosk: KioskContainer = providers.Container(KioskContainer)
    game: GameContainer = providers.Container(GameContainer)
