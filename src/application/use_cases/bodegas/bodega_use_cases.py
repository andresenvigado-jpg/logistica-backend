from src.domain.repositories.bodega_repository import BodegaRepository
from src.domain.entities.bodega import Bodega
from src.domain.exceptions.domain_exceptions import EntityNotFoundException
from src.application.dtos.bodega_dto import BodegaCreateDTO, BodegaUpdateDTO


class ListBodegasUseCase:
    def __init__(self, repo: BodegaRepository):
        self._repo = repo

    def execute(self) -> list[Bodega]:
        return self._repo.find_all()


class GetBodegaUseCase:
    def __init__(self, repo: BodegaRepository):
        self._repo = repo

    def execute(self, id_bodega: int) -> Bodega:
        bodega = self._repo.find_by_id(id_bodega)
        if not bodega:
            raise EntityNotFoundException("Bodega", id_bodega)
        return bodega


class CreateBodegaUseCase:
    def __init__(self, repo: BodegaRepository):
        self._repo = repo

    def execute(self, dto: BodegaCreateDTO) -> Bodega:
        bodega = Bodega(
            id_bodega=None,
            nombre=dto.nombre,
            pais=dto.pais,
            tipo=dto.tipo,
            direccion=dto.direccion,
            ciudad=dto.ciudad,
        )
        return self._repo.save(bodega)


class UpdateBodegaUseCase:
    def __init__(self, repo: BodegaRepository):
        self._repo = repo

    def execute(self, id_bodega: int, dto: BodegaUpdateDTO) -> Bodega:
        bodega = self._repo.find_by_id(id_bodega)
        if not bodega:
            raise EntityNotFoundException("Bodega", id_bodega)
        if dto.nombre is not None:
            bodega.nombre = dto.nombre
        if dto.pais is not None:
            bodega.pais = dto.pais
        if dto.tipo is not None:
            bodega.tipo = dto.tipo
        if dto.direccion is not None:
            bodega.direccion = dto.direccion
        if dto.ciudad is not None:
            bodega.ciudad = dto.ciudad
        return self._repo.update(bodega)


class DeleteBodegaUseCase:
    def __init__(self, repo: BodegaRepository):
        self._repo = repo

    def execute(self, id_bodega: int) -> None:
        if not self._repo.find_by_id(id_bodega):
            raise EntityNotFoundException("Bodega", id_bodega)
        self._repo.delete(id_bodega)
