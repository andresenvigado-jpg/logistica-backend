from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal


@dataclass
class EnvioTerrestre:
    id_envio: int | None
    id_cliente: int
    id_tipo_producto: int
    cantidad: int
    fecha_registro: date
    fecha_entrega: date
    id_bodega: int
    precio_envio: Decimal
    placa: str
    numero_guia: str
    descuento_porcentaje: Decimal = field(default=Decimal("0.00"))
