from abc import ABC, abstractmethod
from src.domain.entities.cliente import Cliente


class ClienteRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[Cliente]: ...

    @abstractmethod
    def find_by_id(self, id_cliente: int) -> Cliente | None: ...

    @abstractmethod
    def find_by_email(self, email: str) -> Cliente | None: ...

    @abstractmethod
    def save(self, cliente: Cliente) -> Cliente: ...

    @abstractmethod
    def update(self, cliente: Cliente) -> Cliente: ...

    @abstractmethod
    def delete(self, id_cliente: int) -> None: ...
