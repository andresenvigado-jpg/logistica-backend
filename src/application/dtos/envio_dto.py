from pydantic import BaseModel, field_validator
from datetime import date
from decimal import Decimal
import re


class EnvioTerrestreCreateDTO(BaseModel):
    id_cliente: int
    id_tipo_producto: int
    cantidad: int
    fecha_registro: date
    fecha_entrega: date
    id_bodega: int
    precio_envio: Decimal
    placa: str
    numero_guia: str

    @field_validator("placa")
    @classmethod
    def validate_placa(cls, v: str) -> str:
        if not re.match(r"^[A-Z]{3}[0-9]{3}$", v.upper()):
            raise ValueError("La placa debe tener formato AAA123 (3 letras + 3 números)")
        return v.upper()

    @field_validator("numero_guia")
    @classmethod
    def validate_guia(cls, v: str) -> str:
        if not re.match(r"^[A-Z0-9]{10}$", v.upper()):
            raise ValueError("El número de guía debe tener exactamente 10 caracteres alfanuméricos")
        return v.upper()

    @field_validator("cantidad")
    @classmethod
    def validate_cantidad(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return v

    @field_validator("precio_envio")
    @classmethod
    def validate_precio(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("El precio de envío debe ser mayor a 0")
        return v


class EnvioTerrestreUpdateDTO(BaseModel):
    id_cliente: int | None = None
    id_tipo_producto: int | None = None
    cantidad: int | None = None
    fecha_entrega: date | None = None
    id_bodega: int | None = None
    precio_envio: Decimal | None = None
    placa: str | None = None


class EnvioTerrestreResponseDTO(BaseModel):
    id_envio: int
    id_cliente: int
    id_tipo_producto: int
    cantidad: int
    fecha_registro: date
    fecha_entrega: date
    id_bodega: int
    precio_envio: Decimal
    descuento_porcentaje: Decimal
    placa: str
    numero_guia: str

    model_config = {"from_attributes": True}


class EnvioMaritimoCreateDTO(BaseModel):
    id_cliente: int
    id_tipo_producto: int
    cantidad: int
    fecha_registro: date
    fecha_entrega: date
    id_puerto: int
    precio_envio: Decimal
    numero_flota: str
    numero_guia: str

    @field_validator("numero_flota")
    @classmethod
    def validate_flota(cls, v: str) -> str:
        if not re.match(r"^[A-Z]{3}[0-9]{4}[A-Z]{1}$", v.upper()):
            raise ValueError("El número de flota debe tener formato AAA1234A (3 letras + 4 números + 1 letra)")
        return v.upper()

    @field_validator("numero_guia")
    @classmethod
    def validate_guia(cls, v: str) -> str:
        if not re.match(r"^[A-Z0-9]{10}$", v.upper()):
            raise ValueError("El número de guía debe tener exactamente 10 caracteres alfanuméricos")
        return v.upper()

    @field_validator("cantidad")
    @classmethod
    def validate_cantidad(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("La cantidad debe ser mayor a 0")
        return v

    @field_validator("precio_envio")
    @classmethod
    def validate_precio(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("El precio de envío debe ser mayor a 0")
        return v


class EnvioMaritimoUpdateDTO(BaseModel):
    id_cliente: int | None = None
    id_tipo_producto: int | None = None
    cantidad: int | None = None
    fecha_entrega: date | None = None
    id_puerto: int | None = None
    precio_envio: Decimal | None = None
    numero_flota: str | None = None


class EnvioMaritimoResponseDTO(BaseModel):
    id_envio: int
    id_cliente: int
    id_tipo_producto: int
    cantidad: int
    fecha_registro: date
    fecha_entrega: date
    id_puerto: int
    precio_envio: Decimal
    descuento_porcentaje: Decimal
    numero_flota: str
    numero_guia: str

    model_config = {"from_attributes": True}
