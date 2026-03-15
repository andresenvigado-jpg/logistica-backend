from sqlalchemy import Column, Integer, String, Text
from src.infrastructure.database.connection import Base


class TipoProductoModel(Base):
    __tablename__ = "tipo_producto"

    id_tipo_producto = Column(Integer, primary_key=True, index=True)
    nombre          = Column(String(100), nullable=False)
    descripcion     = Column(Text, nullable=True)
