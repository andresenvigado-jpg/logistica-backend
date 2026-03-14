from src.domain.repositories.cliente_repository import ClienteRepository
from src.domain.entities.cliente import Cliente
from src.domain.exceptions.domain_exceptions import DuplicateEntityException
from src.application.dtos.cliente_dto import ClienteCreateDTO


class CreateClienteUseCase:
    def __init__(self, repo: ClienteRepository):
        self._repo = repo

    def execute(self, dto: ClienteCreateDTO) -> Cliente:
        if self._repo.find_by_email(dto.email):
            raise DuplicateEntityException("email", dto.email)
        cliente = Cliente(
            id_cliente=None,
            nombre=dto.nombre,
            apellido=dto.apellido,
            email=dto.email,
            telefono=dto.telefono,
            direccion=dto.direccion,
        )
        return self._repo.save(cliente)
