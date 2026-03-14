from sqlalchemy import Column, Integer, String
from src.infrastructure.database.connection import Base


class PuertoModel(Base):
    __tablename__ = "puertos"

    id_puerto = Column(Integer, primary_key=True, index=True)
    nombre    = Column(String(150), nullable=False)
    ciudad    = Column(String(100))
    pais      = Column(String(100), nullable=False)
    tipo      = Column(String(20), nullable=False)
