from dataclasses import dataclass


@dataclass
class Puerto:
    id_puerto: int | None
    nombre: str
    pais: str
    tipo: str
    ciudad: str | None = None
