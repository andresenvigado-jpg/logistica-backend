from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from src.infrastructure.database.connection import Base


class EnvioTerrestreModel(Base):
    __tablename__ = "envio_terrestre"

    id_envio         = Column(Integer, primary_key=True, index=True)
    id_cliente       = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)
    id_tipo_producto = Column(Integer, ForeignKey("tipo_producto.id_tipo_producto"), nullable=False)
    cantidad         = Column(Integer, nullable=False)
    fecha_registro   = Column(Date, nullable=False)
    fecha_entrega    = Column(Date, nullable=False)
    id_bodega        = Column(Integer, ForeignKey("bodegas.id_bodega"), nullable=False)
    precio_envio         = Column(Numeric(12, 2), nullable=False)
    placa                = Column(String(6), nullable=False)
    numero_guia          = Column(String(10), unique=True, nullable=False)
    descuento_porcentaje = Column(Numeric(5, 2), nullable=False, default=0)
