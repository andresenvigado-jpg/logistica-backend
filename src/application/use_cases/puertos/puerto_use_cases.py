from src.domain.repositories.puerto_repository import PuertoRepository
from src.domain.entities.puerto import Puerto
from src.domain.exceptions.domain_exceptions import EntityNotFoundException
from src.application.dtos.puerto_dto import PuertoCreateDTO, PuertoUpdateDTO


class ListPuertosUseCase:
    def __init__(self, repo: PuertoRepository):
        self._repo = repo

    def execute(self) -> list[Puerto]:
        return self._repo.find_all()


class GetPuertoUseCase:
    def __init__(self, repo: PuertoRepository):
        self._repo = repo

    def execute(self, id_puerto: int) -> Puerto:
        puerto = self._repo.find_by_id(id_puerto)
        if not puerto:
            raise EntityNotFoundException("Puerto", id_puerto)
        return puerto


class CreatePuertoUseCase:
    def __init__(self, repo: PuertoRepository):
        self._repo = repo

    def execute(self, dto: PuertoCreateDTO) -> Puerto:
        puerto = Puerto(
            id_puerto=None,
            nombre=dto.nombre,
            pais=dto.pais,
            tipo=dto.tipo,
            ciudad=dto.ciudad,
        )
        return self._repo.save(puerto)


class UpdatePuertoUseCase:
    def __init__(self, repo: PuertoRepository):
        self._repo = repo

    def execute(self, id_puerto: int, dto: PuertoUpdateDTO) -> Puerto:
        puerto = self._repo.find_by_id(id_puerto)
        if not puerto:
            raise EntityNotFoundException("Puerto", id_puerto)
        if dto.nombre is not None:
            puerto.nombre = dto.nombre
        if dto.pais is not None:
            puerto.pais = dto.pais
        if dto.tipo is not None:
            puerto.tipo = dto.tipo
        if dto.ciudad is not None:
            puerto.ciudad = dto.ciudad
        return self._repo.update(puerto)


class DeletePuertoUseCase:
    def __init__(self, repo: PuertoRepository):
        self._repo = repo

    def execute(self, id_puerto: int) -> None:
        if not self._repo.find_by_id(id_puerto):
            raise EntityNotFoundException("Puerto", id_puerto)
        self._repo.delete(id_puerto)
