from sqlalchemy.orm import Session
from src.domain.entities.bodega import Bodega
from src.domain.repositories.bodega_repository import BodegaRepository
from src.infrastructure.database.models.bodega_model import BodegaModel


class BodegaRepositoryImpl(BodegaRepository):
    def __init__(self, db: Session):
        self._db = db

    def find_all(self) -> list[Bodega]:
        return [self._to_entity(r) for r in self._db.query(BodegaModel).all()]

    def find_by_id(self, id_bodega: int) -> Bodega | None:
        row = self._db.query(BodegaModel).filter(BodegaModel.id_bodega == id_bodega).first()
        return self._to_entity(row) if row else None

    def save(self, bodega: Bodega) -> Bodega:
        model = BodegaModel(nombre=bodega.nombre, pais=bodega.pais, tipo=bodega.tipo,
                            direccion=bodega.direccion, ciudad=bodega.ciudad)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def update(self, bodega: Bodega) -> Bodega:
        self._db.query(BodegaModel).filter(BodegaModel.id_bodega == bodega.id_bodega).update({
            "nombre": bodega.nombre, "pais": bodega.pais, "tipo": bodega.tipo,
            "direccion": bodega.direccion, "ciudad": bodega.ciudad,
        })
        self._db.commit()
        return bodega

    def delete(self, id_bodega: int) -> None:
        self._db.query(BodegaModel).filter(BodegaModel.id_bodega == id_bodega).delete()
        self._db.commit()

    @staticmethod
    def _to_entity(m: BodegaModel) -> Bodega:
        return Bodega(id_bodega=m.id_bodega, nombre=m.nombre, pais=m.pais,
                      tipo=m.tipo, direccion=m.direccion, ciudad=m.ciudad)
