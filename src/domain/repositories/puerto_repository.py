from abc import ABC, abstractmethod
from src.domain.entities.puerto import Puerto


class PuertoRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[Puerto]: ...

    @abstractmethod
    def find_by_id(self, id_puerto: int) -> Puerto | None: ...

    @abstractmethod
    def save(self, puerto: Puerto) -> Puerto: ...

    @abstractmethod
    def update(self, puerto: Puerto) -> Puerto: ...

    @abstractmethod
    def delete(self, id_puerto: int) -> None: ...
