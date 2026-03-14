from fastapi import APIRouter, Depends, status
from src.application.dtos.envio_dto import (
    EnvioTerrestreCreateDTO, EnvioTerrestreUpdateDTO, EnvioTerrestreResponseDTO,
    EnvioMaritimoCreateDTO, EnvioMaritimoUpdateDTO, EnvioMaritimoResponseDTO,
)
from src.application.use_cases.envios.envio_use_cases import (
    ListEnviosTerrestreUseCase, GetEnvioTerrestreUseCase,
    CreateEnvioTerrestreUseCase, UpdateEnvioTerrestreUseCase, DeleteEnvioTerrestreUseCase,
    ListEnviosMaritimoUseCase, GetEnvioMaritimoUseCase,
    CreateEnvioMaritimoUseCase, UpdateEnvioMaritimoUseCase, DeleteEnvioMaritimoUseCase,
)
from src.presentation.api.dependencies import (
    get_envio_terrestre_repo, get_envio_maritimo_repo, get_cliente_repo, verify_token
)

router = APIRouter(prefix="/envios", tags=["Envíos"], dependencies=[Depends(verify_token)])

# ── Terrestres ──────────────────────────────────────────────────────────────

@router.get("/terrestres", response_model=list[EnvioTerrestreResponseDTO], summary="Listar envíos terrestres")
def list_terrestres(repo=Depends(get_envio_terrestre_repo)):
    return ListEnviosTerrestreUseCase(repo).execute()


@router.get("/terrestres/{id_envio}", response_model=EnvioTerrestreResponseDTO, summary="Obtener envío terrestre")
def get_terrestre(id_envio: int, repo=Depends(get_envio_terrestre_repo)):
    return GetEnvioTerrestreUseCase(repo).execute(id_envio)


@router.post("/terrestres", response_model=EnvioTerrestreResponseDTO,
             status_code=status.HTTP_201_CREATED, summary="Crear envío terrestre")
def create_terrestre(
    dto: EnvioTerrestreCreateDTO,
    repo=Depends(get_envio_terrestre_repo),
    cliente_repo=Depends(get_cliente_repo),
):
    return CreateEnvioTerrestreUseCase(repo, cliente_repo).execute(dto)


@router.put("/terrestres/{id_envio}", response_model=EnvioTerrestreResponseDTO, summary="Actualizar envío terrestre")
def update_terrestre(id_envio: int, dto: EnvioTerrestreUpdateDTO, repo=Depends(get_envio_terrestre_repo)):
    return UpdateEnvioTerrestreUseCase(repo).execute(id_envio, dto)


@router.delete("/terrestres/{id_envio}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar envío terrestre")
def delete_terrestre(id_envio: int, repo=Depends(get_envio_terrestre_repo)):
    DeleteEnvioTerrestreUseCase(repo).execute(id_envio)


# ── Marítimos ────────────────────────────────────────────────────────────────

@router.get("/maritimos", response_model=list[EnvioMaritimoResponseDTO], summary="Listar envíos marítimos")
def list_maritimos(repo=Depends(get_envio_maritimo_repo)):
    return ListEnviosMaritimoUseCase(repo).execute()


@router.get("/maritimos/{id_envio}", response_model=EnvioMaritimoResponseDTO, summary="Obtener envío marítimo")
def get_maritimo(id_envio: int, repo=Depends(get_envio_maritimo_repo)):
    return GetEnvioMaritimoUseCase(repo).execute(id_envio)


@router.post("/maritimos", response_model=EnvioMaritimoResponseDTO,
             status_code=status.HTTP_201_CREATED, summary="Crear envío marítimo")
def create_maritimo(
    dto: EnvioMaritimoCreateDTO,
    repo=Depends(get_envio_maritimo_repo),
    cliente_repo=Depends(get_cliente_repo),
):
    return CreateEnvioMaritimoUseCase(repo, cliente_repo).execute(dto)


@router.put("/maritimos/{id_envio}", response_model=EnvioMaritimoResponseDTO, summary="Actualizar envío marítimo")
def update_maritimo(id_envio: int, dto: EnvioMaritimoUpdateDTO, repo=Depends(get_envio_maritimo_repo)):
    return UpdateEnvioMaritimoUseCase(repo).execute(id_envio, dto)


@router.delete("/maritimos/{id_envio}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar envío marítimo")
def delete_maritimo(id_envio: int, repo=Depends(get_envio_maritimo_repo)):
    DeleteEnvioMaritimoUseCase(repo).execute(id_envio)
