from sqlalchemy import Column, Integer, String
from src.infrastructure.database.connection import Base


class BodegaModel(Base):
    __tablename__ = "bodegas"

    id_bodega = Column(Integer, primary_key=True, index=True)
    nombre    = Column(String(150), nullable=False)
    direccion = Column(String(250))
    ciudad    = Column(String(100))
    pais      = Column(String(100), nullable=False)
    tipo      = Column(String(20), nullable=False)
