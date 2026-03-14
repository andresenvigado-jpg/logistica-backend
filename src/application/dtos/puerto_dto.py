from pydantic import BaseModel
from typing import Literal


class PuertoCreateDTO(BaseModel):
    nombre: str
    pais: str
    tipo: Literal["nacional", "internacional"]
    ciudad: str | None = None


class PuertoUpdateDTO(BaseModel):
    nombre: str | None = None
    pais: str | None = None
    tipo: Literal["nacional", "internacional"] | None = None
    ciudad: str | None = None


class PuertoResponseDTO(BaseModel):
    id_puerto: int
    nombre: str
    pais: str
    tipo: str
    ciudad: str | None

    model_config = {"from_attributes": True}
