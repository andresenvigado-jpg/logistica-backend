from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from src.infrastructure.database.connection import Base


class UserModel(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    username   = Column(String(50), unique=True, nullable=False)
    email      = Column(String(150), unique=True, nullable=False)
    password   = Column(String(255), nullable=False)
    activo     = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
