from dataclasses import dataclass
from datetime import datetime


@dataclass
class Cliente:
    id_cliente: int | None
    nombre: str
    apellido: str
    email: str
    telefono: str | None = None
    direccion: str | None = None
    created_at: datetime | None = None
