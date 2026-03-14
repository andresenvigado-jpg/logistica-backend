from sqlalchemy.orm import Session
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self._db = db

    def find_by_email(self, email: str) -> User | None:
        row = self._db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_entity(row) if row else None

    def find_by_username(self, username: str) -> User | None:
        row = self._db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_entity(row) if row else None

    def save(self, user: User) -> User:
        model = UserModel(username=user.username, email=user.email, password=user.password)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    @staticmethod
    def _to_entity(m: UserModel) -> User:
        return User(
            id_usuario=m.id_usuario,
            username=m.username,
            email=m.email,
            password=m.password,
            activo=m.activo,
            created_at=m.created_at,
        )
