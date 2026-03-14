from src.domain.repositories.cliente_repository import ClienteRepository
from src.domain.entities.cliente import Cliente
from src.domain.exceptions.domain_exceptions import EntityNotFoundException
from src.application.dtos.cliente_dto import ClienteUpdateDTO


class UpdateClienteUseCase:
    def __init__(self, repo: ClienteRepository):
        self._repo = repo

    def execute(self, id_cliente: int, dto: ClienteUpdateDTO) -> Cliente:
        cliente = self._repo.find_by_id(id_cliente)
        if not cliente:
            raise EntityNotFoundException("Cliente", id_cliente)

        if dto.nombre is not None:
            cliente.nombre = dto.nombre
        if dto.apellido is not None:
            cliente.apellido = dto.apellido
        if dto.email is not None:
            cliente.email = dto.email
        if dto.telefono is not None:
            cliente.telefono = dto.telefono
        if dto.direccion is not None:
            cliente.direccion = dto.direccion

        return self._repo.update(cliente)
