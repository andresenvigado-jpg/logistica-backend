from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parents[4] / ".env")

from src.infrastructure.database.connection import get_db
from src.infrastructure.security.jwt_service import JWTService
from src.infrastructure.security.password_service import PasswordService
from src.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.database.repositories.cliente_repository_impl import ClienteRepositoryImpl
from src.infrastructure.database.repositories.bodega_repository_impl import BodegaRepositoryImpl
from src.infrastructure.database.repositories.puerto_repository_impl import PuertoRepositoryImpl
from src.infrastructure.database.repositories.envio_repository_impl import (
    EnvioTerrestreRepositoryImpl, EnvioMaritimoRepositoryImpl
)
from src.domain.exceptions.domain_exceptions import UnauthorizedException

load_dotenv()

_bearer_scheme = HTTPBearer()


def get_jwt_service() -> JWTService:
    return JWTService(
        secret_key=os.getenv("JWT_SECRET_KEY", "super-secret-key-change-in-production"),
        expire_minutes=int(os.getenv("JWT_EXPIRE_MINUTES", "60")),
    )


def get_password_service() -> PasswordService:
    return PasswordService()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    jwt_service: JWTService = Depends(get_jwt_service),
) -> dict:
    try:
        return jwt_service.decode_token(credentials.credentials)
    except UnauthorizedException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)


def get_user_repo(db: Session = Depends(get_db)):
    return UserRepositoryImpl(db)


def get_cliente_repo(db: Session = Depends(get_db)):
    return ClienteRepositoryImpl(db)


def get_bodega_repo(db: Session = Depends(get_db)):
    return BodegaRepositoryImpl(db)


def get_puerto_repo(db: Session = Depends(get_db)):
    return PuertoRepositoryImpl(db)


def get_envio_terrestre_repo(db: Session = Depends(get_db)):
    return EnvioTerrestreRepositoryImpl(db)


def get_envio_maritimo_repo(db: Session = Depends(get_db)):
    return EnvioMaritimoRepositoryImpl(db)
