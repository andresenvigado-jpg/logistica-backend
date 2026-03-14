from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id_usuario: int | None
    username: str
    email: str
    password: str
    activo: bool = True
    created_at: datetime | None = None
