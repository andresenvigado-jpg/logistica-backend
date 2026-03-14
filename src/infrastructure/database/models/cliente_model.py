from sqlalchemy import Column, Integer, String, DateTime, func
from src.infrastructure.database.connection import Base


class ClienteModel(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True)
    nombre     = Column(String(100), nullable=False)
    apellido   = Column(String(100), nullable=False)
    email      = Column(String(150), unique=True, nullable=False)
    telefono   = Column(String(20))
    direccion  = Column(String(250))
    created_at = Column(DateTime, server_default=func.now())
