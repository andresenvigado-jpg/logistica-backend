from pydantic import BaseModel
from typing import Literal


class BodegaCreateDTO(BaseModel):
    nombre: str
    pais: str
    tipo: Literal["nacional", "internacional"]
    direccion: str | None = None
    ciudad: str | None = None


class BodegaUpdateDTO(BaseModel):
    nombre: str | None = None
    pais: str | None = None
    tipo: Literal["nacional", "internacional"] | None = None
    direccion: str | None = None
    ciudad: str | None = None


class BodegaResponseDTO(BaseModel):
    id_bodega: int
    nombre: str
    pais: str
    tipo: str
    direccion: str | None
    ciudad: str | None

    model_config = {"from_attributes": True}
