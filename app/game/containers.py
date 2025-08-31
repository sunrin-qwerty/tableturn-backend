from dependency_injector import containers, providers

from app.game.repository import GameRepository
from app.game.services import GameService


class GameContainer(containers.DeclarativeContainer):
    repository: GameRepository = providers.Singleton(GameRepository)
    service: GameService = providers.Singleton(
        GameService,
        game_repository=repository,
    )
