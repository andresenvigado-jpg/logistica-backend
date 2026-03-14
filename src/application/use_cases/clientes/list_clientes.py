from src.domain.repositories.cliente_repository import ClienteRepository
from src.domain.entities.cliente import Cliente


class ListClientesUseCase:
    def __init__(self, repo: ClienteRepository):
        self._repo = repo

    def execute(self) -> list[Cliente]:
        return self._repo.find_all()
