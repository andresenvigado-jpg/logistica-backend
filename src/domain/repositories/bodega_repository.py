from abc import ABC, abstractmethod
from src.domain.entities.bodega import Bodega


class BodegaRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[Bodega]: ...

    @abstractmethod
    def find_by_id(self, id_bodega: int) -> Bodega | None: ...

    @abstractmethod
    def save(self, bodega: Bodega) -> Bodega: ...

    @abstractmethod
    def update(self, bodega: Bodega) -> Bodega: ...

    @abstractmethod
    def delete(self, id_bodega: int) -> None: ...
