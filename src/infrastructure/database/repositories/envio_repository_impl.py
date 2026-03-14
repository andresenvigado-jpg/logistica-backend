from sqlalchemy.orm import Session
from src.domain.entities.envio_terrestre import EnvioTerrestre
from src.domain.entities.envio_maritimo import EnvioMaritimo
from src.domain.repositories.envio_repository import EnvioTerrestreRepository, EnvioMaritimoRepository
from src.infrastructure.database.models.envio_terrestre_model import EnvioTerrestreModel
from src.infrastructure.database.models.envio_maritimo_model import EnvioMaritimoModel


class EnvioTerrestreRepositoryImpl(EnvioTerrestreRepository):
    def __init__(self, db: Session):
        self._db = db

    def find_all(self) -> list[EnvioTerrestre]:
        return [self._to_entity(r) for r in self._db.query(EnvioTerrestreModel).all()]

    def find_by_id(self, id_envio: int) -> EnvioTerrestre | None:
        row = self._db.query(EnvioTerrestreModel).filter(EnvioTerrestreModel.id_envio == id_envio).first()
        return self._to_entity(row) if row else None

    def find_by_numero_guia(self, numero_guia: str) -> EnvioTerrestre | None:
        row = self._db.query(EnvioTerrestreModel).filter(EnvioTerrestreModel.numero_guia == numero_guia).first()
        return self._to_entity(row) if row else None

    def save(self, envio: EnvioTerrestre) -> EnvioTerrestre:
        model = EnvioTerrestreModel(
            id_cliente=envio.id_cliente, id_tipo_producto=envio.id_tipo_producto,
            cantidad=envio.cantidad, fecha_registro=envio.fecha_registro,
            fecha_entrega=envio.fecha_entrega, id_bodega=envio.id_bodega,
            precio_envio=envio.precio_envio, placa=envio.placa, numero_guia=envio.numero_guia,
            descuento_porcentaje=envio.descuento_porcentaje,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def update(self, envio: EnvioTerrestre) -> EnvioTerrestre:
        self._db.query(EnvioTerrestreModel).filter(EnvioTerrestreModel.id_envio == envio.id_envio).update({
            "id_cliente": envio.id_cliente, "id_tipo_producto": envio.id_tipo_producto,
            "cantidad": envio.cantidad, "fecha_entrega": envio.fecha_entrega,
            "id_bodega": envio.id_bodega, "precio_envio": envio.precio_envio, "placa": envio.placa,
        })
        self._db.commit()
        return envio

    def delete(self, id_envio: int) -> None:
        self._db.query(EnvioTerrestreModel).filter(EnvioTerrestreModel.id_envio == id_envio).delete()
        self._db.commit()

    @staticmethod
    def _to_entity(m: EnvioTerrestreModel) -> EnvioTerrestre:
        return EnvioTerrestre(
            id_envio=m.id_envio, id_cliente=m.id_cliente, id_tipo_producto=m.id_tipo_producto,
            cantidad=m.cantidad, fecha_registro=m.fecha_registro, fecha_entrega=m.fecha_entrega,
            id_bodega=m.id_bodega, precio_envio=m.precio_envio, placa=m.placa, numero_guia=m.numero_guia,
            descuento_porcentaje=m.descuento_porcentaje,
        )


class EnvioMaritimoRepositoryImpl(EnvioMaritimoRepository):
    def __init__(self, db: Session):
        self._db = db

    def find_all(self) -> list[EnvioMaritimo]:
        return [self._to_entity(r) for r in self._db.query(EnvioMaritimoModel).all()]

    def find_by_id(self, id_envio: int) -> EnvioMaritimo | None:
        row = self._db.query(EnvioMaritimoModel).filter(EnvioMaritimoModel.id_envio == id_envio).first()
        return self._to_entity(row) if row else None

    def find_by_numero_guia(self, numero_guia: str) -> EnvioMaritimo | None:
        row = self._db.query(EnvioMaritimoModel).filter(EnvioMaritimoModel.numero_guia == numero_guia).first()
        return self._to_entity(row) if row else None

    def save(self, envio: EnvioMaritimo) -> EnvioMaritimo:
        model = EnvioMaritimoModel(
            id_cliente=envio.id_cliente, id_tipo_producto=envio.id_tipo_producto,
            cantidad=envio.cantidad, fecha_registro=envio.fecha_registro,
            fecha_entrega=envio.fecha_entrega, id_puerto=envio.id_puerto,
            precio_envio=envio.precio_envio, numero_flota=envio.numero_flota, numero_guia=envio.numero_guia,
            descuento_porcentaje=envio.descuento_porcentaje,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def update(self, envio: EnvioMaritimo) -> EnvioMaritimo:
        self._db.query(EnvioMaritimoModel).filter(EnvioMaritimoModel.id_envio == envio.id_envio).update({
            "id_cliente": envio.id_cliente, "id_tipo_producto": envio.id_tipo_producto,
            "cantidad": envio.cantidad, "fecha_entrega": envio.fecha_entrega,
            "id_puerto": envio.id_puerto, "precio_envio": envio.precio_envio, "numero_flota": envio.numero_flota,
        })
        self._db.commit()
        return envio

    def delete(self, id_envio: int) -> None:
        self._db.query(EnvioMaritimoModel).filter(EnvioMaritimoModel.id_envio == id_envio).delete()
        self._db.commit()

    @staticmethod
    def _to_entity(m: EnvioMaritimoModel) -> EnvioMaritimo:
        return EnvioMaritimo(
            id_envio=m.id_envio, id_cliente=m.id_cliente, id_tipo_producto=m.id_tipo_producto,
            cantidad=m.cantidad, fecha_registro=m.fecha_registro, fecha_entrega=m.fecha_entrega,
            id_puerto=m.id_puerto, precio_envio=m.precio_envio, numero_flota=m.numero_flota, numero_guia=m.numero_guia,
            descuento_porcentaje=m.descuento_porcentaje,
        )
