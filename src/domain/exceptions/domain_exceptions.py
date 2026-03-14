class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class EntityNotFoundException(DomainException):
    def __init__(self, entity: str, entity_id: int):
        super().__init__(f"{entity} con id {entity_id} no encontrado", status_code=404)


class DuplicateEntityException(DomainException):
    def __init__(self, field: str, value: str):
        super().__init__(f"Ya existe un registro con {field}: {value}", status_code=400)


class InvalidCredentialsException(DomainException):
    def __init__(self):
        super().__init__("Credenciales inválidas", status_code=401)


class UnauthorizedException(DomainException):
    def __init__(self, message: str = "No autorizado"):
        super().__init__(message, status_code=401)
