from decimal import Decimal
from src.domain.repositories.envio_repository import EnvioTerrestreRepository, EnvioMaritimoRepository
from src.domain.repositories.cliente_repository import ClienteRepository
from src.domain.entities.envio_terrestre import EnvioTerrestre
from src.domain.entities.envio_maritimo import EnvioMaritimo
from src.domain.exceptions.domain_exceptions import (
    EntityNotFoundException, DomainException, DuplicateEntityException
)
from src.application.dtos.envio_dto import (
    EnvioTerrestreCreateDTO, EnvioTerrestreUpdateDTO,
    EnvioMaritimoCreateDTO, EnvioMaritimoUpdateDTO,
)

# ── Constantes de descuento ─────────────────────────────────────────────────
DESCUENTO_TERRESTRE = Decimal("5.00")   # 5% si cantidad > 10
DESCUENTO_MARITIMO  = Decimal("3.00")   # 3% si cantidad > 10
CANTIDAD_MINIMA_DESCUENTO = 10


class ListEnviosTerrestreUseCase:
    def __init__(self, repo: EnvioTerrestreRepository):
        self._repo = repo

    def execute(self) -> list[EnvioTerrestre]:
        return self._repo.find_all()


class GetEnvioTerrestreUseCase:
    def __init__(self, repo: EnvioTerrestreRepository):
        self._repo = repo

    def execute(self, id_envio: int) -> EnvioTerrestre:
        envio = self._repo.find_by_id(id_envio)
        if not envio:
            raise EntityNotFoundException("Envío Terrestre", id_envio)
        return envio


class CreateEnvioTerrestreUseCase:
    def __init__(self, repo: EnvioTerrestreRepository, cliente_repo: ClienteRepository):
        self._repo = repo
        self._cliente_repo = cliente_repo

    def execute(self, dto: EnvioTerrestreCreateDTO) -> EnvioTerrestre:
        # 1. Validar que el cliente exista
        if not self._cliente_repo.find_by_id(dto.id_cliente):
            raise EntityNotFoundException("Cliente", dto.id_cliente)

        # 2. Validar unicidad del número de guía
        if self._repo.find_by_numero_guia(dto.numero_guia):
            raise DuplicateEntityException("numero_guia", dto.numero_guia)

        # 3. Validar fechas
        if dto.fecha_entrega < dto.fecha_registro:
            raise DomainException("La fecha de entrega no puede ser anterior a la fecha de registro")

        # 4. Aplicar descuento del 5% si cantidad > 10 (logística terrestre)
        descuento_porcentaje = Decimal("0.00")
        precio_final = dto.precio_envio
        if dto.cantidad > CANTIDAD_MINIMA_DESCUENTO:
            descuento_porcentaje = DESCUENTO_TERRESTRE
            precio_final = dto.precio_envio * (1 - descuento_porcentaje / 100)
            precio_final = precio_final.quantize(Decimal("0.01"))

        envio = EnvioTerrestre(
            id_envio=None,
            id_cliente=dto.id_cliente,
            id_tipo_producto=dto.id_tipo_producto,
            cantidad=dto.cantidad,
            fecha_registro=dto.fecha_registro,
            fecha_entrega=dto.fecha_entrega,
            id_bodega=dto.id_bodega,
            precio_envio=precio_final,
            placa=dto.placa,
            numero_guia=dto.numero_guia,
            descuento_porcentaje=descuento_porcentaje,
        )
        return self._repo.save(envio)


class UpdateEnvioTerrestreUseCase:
    def __init__(self, repo: EnvioTerrestreRepository):
        self._repo = repo

    def execute(self, id_envio: int, dto: EnvioTerrestreUpdateDTO) -> EnvioTerrestre:
        envio = self._repo.find_by_id(id_envio)
        if not envio:
            raise EntityNotFoundException("Envío Terrestre", id_envio)
        if dto.id_cliente is not None:
            envio.id_cliente = dto.id_cliente
        if dto.id_tipo_producto is not None:
            envio.id_tipo_producto = dto.id_tipo_producto
        if dto.cantidad is not None:
            envio.cantidad = dto.cantidad
        if dto.fecha_entrega is not None:
            envio.fecha_entrega = dto.fecha_entrega
        if dto.id_bodega is not None:
            envio.id_bodega = dto.id_bodega
        if dto.precio_envio is not None:
            envio.precio_envio = dto.precio_envio
        if dto.placa is not None:
            envio.placa = dto.placa
        return self._repo.update(envio)


class DeleteEnvioTerrestreUseCase:
    def __init__(self, repo: EnvioTerrestreRepository):
        self._repo = repo

    def execute(self, id_envio: int) -> None:
        if not self._repo.find_by_id(id_envio):
            raise EntityNotFoundException("Envío Terrestre", id_envio)
        self._repo.delete(id_envio)


class ListEnviosMaritimoUseCase:
    def __init__(self, repo: EnvioMaritimoRepository):
        self._repo = repo

    def execute(self) -> list[EnvioMaritimo]:
        return self._repo.find_all()


class GetEnvioMaritimoUseCase:
    def __init__(self, repo: EnvioMaritimoRepository):
        self._repo = repo

    def execute(self, id_envio: int) -> EnvioMaritimo:
        envio = self._repo.find_by_id(id_envio)
        if not envio:
            raise EntityNotFoundException("Envío Marítimo", id_envio)
        return envio


class CreateEnvioMaritimoUseCase:
    def __init__(self, repo: EnvioMaritimoRepository, cliente_repo: ClienteRepository):
        self._repo = repo
        self._cliente_repo = cliente_repo

    def execute(self, dto: EnvioMaritimoCreateDTO) -> EnvioMaritimo:
        # 1. Validar que el cliente exista
        if not self._cliente_repo.find_by_id(dto.id_cliente):
            raise EntityNotFoundException("Cliente", dto.id_cliente)

        # 2. Validar unicidad del número de guía
        if self._repo.find_by_numero_guia(dto.numero_guia):
            raise DuplicateEntityException("numero_guia", dto.numero_guia)

        # 3. Validar fechas
        if dto.fecha_entrega < dto.fecha_registro:
            raise DomainException("La fecha de entrega no puede ser anterior a la fecha de registro")

        # 4. Aplicar descuento del 3% si cantidad > 10 (logística marítima)
        descuento_porcentaje = Decimal("0.00")
        precio_final = dto.precio_envio
        if dto.cantidad > CANTIDAD_MINIMA_DESCUENTO:
            descuento_porcentaje = DESCUENTO_MARITIMO
            precio_final = dto.precio_envio * (1 - descuento_porcentaje / 100)
            precio_final = precio_final.quantize(Decimal("0.01"))

        envio = EnvioMaritimo(
            id_envio=None,
            id_cliente=dto.id_cliente,
            id_tipo_producto=dto.id_tipo_producto,
            cantidad=dto.cantidad,
            fecha_registro=dto.fecha_registro,
            fecha_entrega=dto.fecha_entrega,
            id_puerto=dto.id_puerto,
            precio_envio=precio_final,
            numero_flota=dto.numero_flota,
            numero_guia=dto.numero_guia,
            descuento_porcentaje=descuento_porcentaje,
        )
        return self._repo.save(envio)


class UpdateEnvioMaritimoUseCase:
    def __init__(self, repo: EnvioMaritimoRepository):
        self._repo = repo

    def execute(self, id_envio: int, dto: EnvioMaritimoUpdateDTO) -> EnvioMaritimo:
        envio = self._repo.find_by_id(id_envio)
        if not envio:
            raise EntityNotFoundException("Envío Marítimo", id_envio)
        if dto.id_cliente is not None:
            envio.id_cliente = dto.id_cliente
        if dto.id_tipo_producto is not None:
            envio.id_tipo_producto = dto.id_tipo_producto
        if dto.cantidad is not None:
            envio.cantidad = dto.cantidad
        if dto.fecha_entrega is not None:
            envio.fecha_entrega = dto.fecha_entrega
        if dto.id_puerto is not None:
            envio.id_puerto = dto.id_puerto
        if dto.precio_envio is not None:
            envio.precio_envio = dto.precio_envio
        if dto.numero_flota is not None:
            envio.numero_flota = dto.numero_flota
        return self._repo.update(envio)


class DeleteEnvioMaritimoUseCase:
    def __init__(self, repo: EnvioMaritimoRepository):
        self._repo = repo

    def execute(self, id_envio: int) -> None:
        if not self._repo.find_by_id(id_envio):
            raise EntityNotFoundException("Envío Marítimo", id_envio)
        self._repo.delete(id_envio)
