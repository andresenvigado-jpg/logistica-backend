from src.domain.repositories.cliente_repository import ClienteRepository
from src.domain.exceptions.domain_exceptions import EntityNotFoundException


class DeleteClienteUseCase:
    def __init__(self, repo: ClienteRepository):
        self._repo = repo

    def execute(self, id_cliente: int) -> None:
        if not self._repo.find_by_id(id_cliente):
            raise EntityNotFoundException("Cliente", id_cliente)
        self._repo.delete(id_cliente)
