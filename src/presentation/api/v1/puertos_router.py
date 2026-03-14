from fastapi import APIRouter, Depends, status
from src.application.dtos.puerto_dto import PuertoCreateDTO, PuertoUpdateDTO, PuertoResponseDTO
from src.application.use_cases.puertos.puerto_use_cases import (
    ListPuertosUseCase, GetPuertoUseCase, CreatePuertoUseCase, UpdatePuertoUseCase, DeletePuertoUseCase
)
from src.presentation.api.dependencies import get_puerto_repo, verify_token

router = APIRouter(prefix="/puertos", tags=["Puertos"], dependencies=[Depends(verify_token)])


@router.get("/", response_model=list[PuertoResponseDTO], summary="Listar puertos")
def list_puertos(repo=Depends(get_puerto_repo)):
    return ListPuertosUseCase(repo).execute()


@router.get("/{id_puerto}", response_model=PuertoResponseDTO, summary="Obtener puerto por ID")
def get_puerto(id_puerto: int, repo=Depends(get_puerto_repo)):
    return GetPuertoUseCase(repo).execute(id_puerto)


@router.post("/", response_model=PuertoResponseDTO, status_code=status.HTTP_201_CREATED, summary="Crear puerto")
def create_puerto(dto: PuertoCreateDTO, repo=Depends(get_puerto_repo)):
    return CreatePuertoUseCase(repo).execute(dto)


@router.put("/{id_puerto}", response_model=PuertoResponseDTO, summary="Actualizar puerto")
def update_puerto(id_puerto: int, dto: PuertoUpdateDTO, repo=Depends(get_puerto_repo)):
    return UpdatePuertoUseCase(repo).execute(id_puerto, dto)


@router.delete("/{id_puerto}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar puerto")
def delete_puerto(id_puerto: int, repo=Depends(get_puerto_repo)):
    DeletePuertoUseCase(repo).execute(id_puerto)
