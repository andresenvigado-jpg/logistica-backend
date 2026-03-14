from dataclasses import dataclass


@dataclass
class Bodega:
    id_bodega: int | None
    nombre: str
    pais: str
    tipo: str
    direccion: str | None = None
    ciudad: str | None = None
