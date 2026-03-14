from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.exceptions.domain_exceptions import DuplicateEntityException
from src.application.dtos.auth_dto import RegisterDTO
from src.infrastructure.security.password_service import PasswordService


class RegisterUserUseCase:
    def __init__(self, user_repo: UserRepository, password_service: PasswordService):
        self._user_repo = user_repo
        self._password_service = password_service

    def execute(self, dto: RegisterDTO) -> User:
        if self._user_repo.find_by_email(dto.email):
            raise DuplicateEntityException("email", dto.email)
        if self._user_repo.find_by_username(dto.username):
            raise DuplicateEntityException("username", dto.username)

        user = User(
            id_usuario=None,
            username=dto.username,
            email=dto.email,
            password=self._password_service.hash(dto.password),
        )
        return self._user_repo.save(user)
