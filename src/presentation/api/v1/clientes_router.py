from fastapi import APIRouter, Depends, status
from src.application.dtos.cliente_dto import ClienteCreateDTO, ClienteUpdateDTO, ClienteResponseDTO
from src.application.use_cases.clientes.list_clientes import ListClientesUseCase
from src.application.use_cases.clientes.get_cliente import GetClienteUseCase
from src.application.use_cases.clientes.create_cliente import CreateClienteUseCase
from src.application.use_cases.clientes.update_cliente import UpdateClienteUseCase
from src.application.use_cases.clientes.delete_cliente import DeleteClienteUseCase
from src.presentation.api.dependencies import get_cliente_repo, verify_token

router = APIRouter(prefix="/clientes", tags=["Clientes"], dependencies=[Depends(verify_token)])


@router.get("/", response_model=list[ClienteResponseDTO], summary="Listar todos los clientes")
def list_clientes(repo=Depends(get_cliente_repo)):
    return ListClientesUseCase(repo).execute()


@router.get("/{id_cliente}", response_model=ClienteResponseDTO, summary="Obtener cliente por ID")
def get_cliente(id_cliente: int, repo=Depends(get_cliente_repo)):
    return GetClienteUseCase(repo).execute(id_cliente)


@router.post("/", response_model=ClienteResponseDTO, status_code=status.HTTP_201_CREATED, summary="Crear cliente")
def create_cliente(dto: ClienteCreateDTO, repo=Depends(get_cliente_repo)):
    return CreateClienteUseCase(repo).execute(dto)


@router.put("/{id_cliente}", response_model=ClienteResponseDTO, summary="Actualizar cliente")
def update_cliente(id_cliente: int, dto: ClienteUpdateDTO, repo=Depends(get_cliente_repo)):
    return UpdateClienteUseCase(repo).execute(id_cliente, dto)


@router.delete("/{id_cliente}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar cliente")
def delete_cliente(id_cliente: int, repo=Depends(get_cliente_repo)):
    DeleteClienteUseCase(repo).execute(id_cliente)
