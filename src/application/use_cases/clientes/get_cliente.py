from src.domain.repositories.cliente_repository import ClienteRepository
from src.domain.entities.cliente import Cliente
from src.domain.exceptions.domain_exceptions import EntityNotFoundException


class GetClienteUseCase:
    def __init__(self, repo: ClienteRepository):
        self._repo = repo

    def execute(self, id_cliente: int) -> Cliente:
        cliente = self._repo.find_by_id(id_cliente)
        if not cliente:
            raise EntityNotFoundException("Cliente", id_cliente)
        return cliente
