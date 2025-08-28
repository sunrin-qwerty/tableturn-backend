from dependency_injector import containers, providers

from app.kiosk.repository import KioskRepository
from app.kiosk.services import KioskService


class KioskContainer(containers.DeclarativeContainer):
    repository: KioskRepository = providers.Singleton(KioskRepository)
    service: KioskService = providers.Singleton(
        KioskService,
        kiosk_repository=repository,
    )
