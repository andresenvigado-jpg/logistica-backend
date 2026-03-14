from abc import ABC, abstractmethod
from src.domain.entities.envio_terrestre import EnvioTerrestre
from src.domain.entities.envio_maritimo import EnvioMaritimo


class EnvioTerrestreRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[EnvioTerrestre]: ...

    @abstractmethod
    def find_by_id(self, id_envio: int) -> EnvioTerrestre | None: ...

    @abstractmethod
    def find_by_numero_guia(self, numero_guia: str) -> EnvioTerrestre | None: ...

    @abstractmethod
    def save(self, envio: EnvioTerrestre) -> EnvioTerrestre: ...

    @abstractmethod
    def update(self, envio: EnvioTerrestre) -> EnvioTerrestre: ...

    @abstractmethod
    def delete(self, id_envio: int) -> None: ...


class EnvioMaritimoRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[EnvioMaritimo]: ...

    @abstractmethod
    def find_by_id(self, id_envio: int) -> EnvioMaritimo | None: ...

    @abstractmethod
    def find_by_numero_guia(self, numero_guia: str) -> EnvioMaritimo | None: ...

    @abstractmethod
    def save(self, envio: EnvioMaritimo) -> EnvioMaritimo: ...

    @abstractmethod
    def update(self, envio: EnvioMaritimo) -> EnvioMaritimo: ...

    @abstractmethod
    def delete(self, id_envio: int) -> None: ...
