from pydantic import BaseModel, EmailStr
from datetime import datetime


class ClienteCreateDTO(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    telefono: str | None = None
    direccion: str | None = None


class ClienteUpdateDTO(BaseModel):
    nombre: str | None = None
    apellido: str | None = None
    email: EmailStr | None = None
    telefono: str | None = None
    direccion: str | None = None


class ClienteResponseDTO(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    email: str
    telefono: str | None
    direccion: str | None
    created_at: datetime | None

    model_config = {"from_attributes": True}
