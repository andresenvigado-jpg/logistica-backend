from sqlalchemy.orm import Session
from src.domain.entities.cliente import Cliente
from src.domain.repositories.cliente_repository import ClienteRepository
from src.infrastructure.database.models.cliente_model import ClienteModel


class ClienteRepositoryImpl(ClienteRepository):
    def __init__(self, db: Session):
        self._db = db

    def find_all(self) -> list[Cliente]:
        return [self._to_entity(r) for r in self._db.query(ClienteModel).all()]

    def find_by_id(self, id_cliente: int) -> Cliente | None:
        row = self._db.query(ClienteModel).filter(ClienteModel.id_cliente == id_cliente).first()
        return self._to_entity(row) if row else None

    def find_by_email(self, email: str) -> Cliente | None:
        row = self._db.query(ClienteModel).filter(ClienteModel.email == email).first()
        return self._to_entity(row) if row else None

    def save(self, cliente: Cliente) -> Cliente:
        model = ClienteModel(
            nombre=cliente.nombre, apellido=cliente.apellido,
            email=cliente.email, telefono=cliente.telefono, direccion=cliente.direccion,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def update(self, cliente: Cliente) -> Cliente:
        self._db.query(ClienteModel).filter(ClienteModel.id_cliente == cliente.id_cliente).update({
            "nombre": cliente.nombre, "apellido": cliente.apellido,
            "email": cliente.email, "telefono": cliente.telefono, "direccion": cliente.direccion,
        })
        self._db.commit()
        return cliente

    def delete(self, id_cliente: int) -> None:
        self._db.query(ClienteModel).filter(ClienteModel.id_cliente == id_cliente).delete()
        self._db.commit()

    @staticmethod
    def _to_entity(m: ClienteModel) -> Cliente:
        return Cliente(
            id_cliente=m.id_cliente, nombre=m.nombre, apellido=m.apellido,
            email=m.email, telefono=m.telefono, direccion=m.direccion, created_at=m.created_at,
        )
