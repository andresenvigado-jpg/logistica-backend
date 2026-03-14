from fastapi import APIRouter, Depends, status
from src.application.dtos.bodega_dto import BodegaCreateDTO, BodegaUpdateDTO, BodegaResponseDTO
from src.application.use_cases.bodegas.bodega_use_cases import (
    ListBodegasUseCase, GetBodegaUseCase, CreateBodegaUseCase, UpdateBodegaUseCase, DeleteBodegaUseCase
)
from src.presentation.api.dependencies import get_bodega_repo, verify_token

router = APIRouter(prefix="/bodegas", tags=["Bodegas"], dependencies=[Depends(verify_token)])


@router.get("/", response_model=list[BodegaResponseDTO], summary="Listar bodegas")
def list_bodegas(repo=Depends(get_bodega_repo)):
    return ListBodegasUseCase(repo).execute()


@router.get("/{id_bodega}", response_model=BodegaResponseDTO, summary="Obtener bodega por ID")
def get_bodega(id_bodega: int, repo=Depends(get_bodega_repo)):
    return GetBodegaUseCase(repo).execute(id_bodega)


@router.post("/", response_model=BodegaResponseDTO, status_code=status.HTTP_201_CREATED, summary="Crear bodega")
def create_bodega(dto: BodegaCreateDTO, repo=Depends(get_bodega_repo)):
    return CreateBodegaUseCase(repo).execute(dto)


@router.put("/{id_bodega}", response_model=BodegaResponseDTO, summary="Actualizar bodega")
def update_bodega(id_bodega: int, dto: BodegaUpdateDTO, repo=Depends(get_bodega_repo)):
    return UpdateBodegaUseCase(repo).execute(id_bodega, dto)


@router.delete("/{id_bodega}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar bodega")
def delete_bodega(id_bodega: int, repo=Depends(get_bodega_repo)):
    DeleteBodegaUseCase(repo).execute(id_bodega)
