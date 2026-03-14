from sqlalchemy.orm import Session
from src.domain.entities.puerto import Puerto
from src.domain.repositories.puerto_repository import PuertoRepository
from src.infrastructure.database.models.puerto_model import PuertoModel


class PuertoRepositoryImpl(PuertoRepository):
    def __init__(self, db: Session):
        self._db = db

    def find_all(self) -> list[Puerto]:
        return [self._to_entity(r) for r in self._db.query(PuertoModel).all()]

    def find_by_id(self, id_puerto: int) -> Puerto | None:
        row = self._db.query(PuertoModel).filter(PuertoModel.id_puerto == id_puerto).first()
        return self._to_entity(row) if row else None

    def save(self, puerto: Puerto) -> Puerto:
        model = PuertoModel(nombre=puerto.nombre, pais=puerto.pais,
                            tipo=puerto.tipo, ciudad=puerto.ciudad)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def update(self, puerto: Puerto) -> Puerto:
        self._db.query(PuertoModel).filter(PuertoModel.id_puerto == puerto.id_puerto).update({
            "nombre": puerto.nombre, "pais": puerto.pais,
            "tipo": puerto.tipo, "ciudad": puerto.ciudad,
        })
        self._db.commit()
        return puerto

    def delete(self, id_puerto: int) -> None:
        self._db.query(PuertoModel).filter(PuertoModel.id_puerto == id_puerto).delete()
        self._db.commit()

    @staticmethod
    def _to_entity(m: PuertoModel) -> Puerto:
        return Puerto(id_puerto=m.id_puerto, nombre=m.nombre,
                      pais=m.pais, tipo=m.tipo, ciudad=m.ciudad)
