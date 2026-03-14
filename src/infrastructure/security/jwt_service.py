from datetime import datetime, timedelta, timezone
import jwt
from src.domain.exceptions.domain_exceptions import UnauthorizedException


class JWTService:
    def __init__(self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 60):
        self._secret = secret_key
        self._algorithm = algorithm
        self._expire_minutes = expire_minutes

    def create_token(self, payload: dict) -> str:
        data = payload.copy()
        data["exp"] = datetime.now(timezone.utc) + timedelta(minutes=self._expire_minutes)
        return jwt.encode(data, self._secret, algorithm=self._algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self._secret, algorithms=[self._algorithm])
        except jwt.ExpiredSignatureError:
            raise UnauthorizedException("Token expirado")
        except jwt.InvalidTokenError:
            raise UnauthorizedException("Token inválido")
