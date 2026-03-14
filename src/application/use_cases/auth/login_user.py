from src.domain.repositories.user_repository import UserRepository
from src.domain.exceptions.domain_exceptions import InvalidCredentialsException
from src.application.dtos.auth_dto import LoginDTO, TokenResponseDTO
from src.infrastructure.security.password_service import PasswordService
from src.infrastructure.security.jwt_service import JWTService


class LoginUserUseCase:
    def __init__(self, user_repo: UserRepository, password_service: PasswordService, jwt_service: JWTService):
        self._user_repo = user_repo
        self._password_service = password_service
        self._jwt_service = jwt_service

    def execute(self, dto: LoginDTO) -> TokenResponseDTO:
        user = self._user_repo.find_by_email(dto.email)
        if not user or not self._password_service.verify(dto.password, user.password):
            raise InvalidCredentialsException()

        token = self._jwt_service.create_token({"sub": str(user.id_usuario), "email": user.email})
        return TokenResponseDTO(access_token=token)
