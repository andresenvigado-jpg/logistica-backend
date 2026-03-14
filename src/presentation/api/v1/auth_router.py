from fastapi import APIRouter, Depends, status
from src.application.dtos.auth_dto import RegisterDTO, LoginDTO, TokenResponseDTO
from src.application.use_cases.auth.register_user import RegisterUserUseCase
from src.application.use_cases.auth.login_user import LoginUserUseCase
from src.presentation.api.dependencies import get_user_repo, get_jwt_service, get_password_service

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", status_code=status.HTTP_201_CREATED, summary="Registrar nuevo usuario")
def register(dto: RegisterDTO, user_repo=Depends(get_user_repo), password_service=Depends(get_password_service)):
    use_case = RegisterUserUseCase(user_repo, password_service)
    user = use_case.execute(dto)
    return {"message": "Usuario registrado exitosamente", "id_usuario": user.id_usuario, "username": user.username}


@router.post("/login", response_model=TokenResponseDTO, summary="Iniciar sesión y obtener token Bearer")
def login(dto: LoginDTO, user_repo=Depends(get_user_repo),
          password_service=Depends(get_password_service), jwt_service=Depends(get_jwt_service)):
    use_case = LoginUserUseCase(user_repo, password_service, jwt_service)
    return use_case.execute(dto)
