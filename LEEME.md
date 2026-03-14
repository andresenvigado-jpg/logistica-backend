# Backend - Sistema de Gestión Logística
## Guía completa para desarrolladores Junior

---

## ¿Qué es este proyecto?

Es una **API REST** que permite gestionar envíos logísticos terrestres y marítimos.
Fue construida con **Python + FastAPI** siguiendo una arquitectura profesional llamada **Clean Architecture**.

Una API REST es básicamente un servidor que recibe peticiones HTTP (como las que hace un navegador o una app móvil) y responde con datos en formato JSON.

---

## Tecnologías utilizadas

| Tecnología | ¿Para qué sirve? |
|-----------|-----------------|
| **Python 3.12+** | Lenguaje de programación principal |
| **FastAPI** | Framework para construir APIs REST. Genera Swagger automáticamente |
| **SQLAlchemy** | ORM - Permite hablar con la base de datos usando Python en vez de SQL puro |
| **PostgreSQL** | Base de datos relacional donde se guarda toda la información |
| **PyJWT** | Genera y valida tokens de seguridad (JWT) |
| **bcrypt** | Encripta las contraseñas antes de guardarlas |
| **Pydantic** | Valida que los datos recibidos tengan el formato correcto |
| **Uvicorn** | Servidor web que corre la aplicación |
| **python-dotenv** | Lee variables de configuración desde el archivo `.env` |

---

## Estructura de carpetas explicada

```
logistica_backend/
│
├── main.py                          ← Punto de entrada. Aquí arranca todo
├── requirements.txt                 ← Lista de librerías necesarias
├── .env                             ← Variables de configuración (NO subir a Git)
├── .env.example                     ← Plantilla del .env para otros desarrolladores
│
└── src/                             ← Todo el código fuente está aquí
    ├── domain/                      ← CAPA 1: El corazón del sistema
    ├── application/                 ← CAPA 2: La lógica de negocio
    ├── infrastructure/              ← CAPA 3: Base de datos y seguridad
    └── presentation/                ← CAPA 4: Las APIs que expone el servidor
```

---

## ¿Qué es Clean Architecture?

Imagina una **cebolla** con varias capas. Las capas internas no saben nada de las externas:

```
┌─────────────────────────────────────┐
│           PRESENTATION              │  ← Capa 4: Routers, endpoints HTTP
│  ┌───────────────────────────────┐  │
│  │        INFRASTRUCTURE         │  │  ← Capa 3: Base de datos, JWT, bcrypt
│  │  ┌─────────────────────────┐  │  │
│  │  │      APPLICATION        │  │  │  ← Capa 2: Casos de uso (lógica)
│  │  │  ┌───────────────────┐  │  │  │
│  │  │  │      DOMAIN       │  │  │  │  ← Capa 1: Entidades y contratos
│  │  │  └───────────────────┘  │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Regla de oro:** Las dependencias siempre van hacia adentro.
- `Presentation` conoce a `Application`
- `Application` conoce a `Domain`
- `Domain` no conoce a nadie (es independiente)
- `Infrastructure` implementa lo que `Domain` define

**¿Por qué es útil?** Si mañana cambias PostgreSQL por MySQL, solo tocas la capa Infrastructure. El resto del código no cambia.

---

## CAPA 1 — Domain (El corazón)

```
src/domain/
├── entities/           ← Objetos que representan el negocio
│   ├── user.py
│   ├── cliente.py
│   ├── bodega.py
│   ├── puerto.py
│   ├── envio_terrestre.py
│   └── envio_maritimo.py
├── repositories/       ← Contratos (interfaces abstractas)
│   ├── user_repository.py
│   ├── cliente_repository.py
│   ├── bodega_repository.py
│   ├── puerto_repository.py
│   └── envio_repository.py
└── exceptions/         ← Errores propios del negocio
    └── domain_exceptions.py
```

### ¿Qué es una entidad?

Una entidad es un objeto Python puro que representa algo del mundo real.
No tiene conexión con la base de datos, solo tiene datos.

```python
# src/domain/entities/cliente.py
@dataclass
class Cliente:
    id_cliente: int | None   # None cuando aún no se ha guardado
    nombre: str
    apellido: str
    email: str
    telefono: str | None = None
    direccion: str | None = None
```

### ¿Qué es un repositorio abstracto?

Es un **contrato** que define qué operaciones se pueden hacer, pero NO dice cómo hacerlas.
Es como decir "quiero un método que busque un cliente por ID" sin importar si lo busca en PostgreSQL, MySQL o un archivo de texto.

```python
# src/domain/repositories/cliente_repository.py
class ClienteRepository(ABC):        # ABC = Clase Abstracta
    @abstractmethod
    def find_by_id(self, id: int) -> Cliente | None: ...  # Solo el contrato, sin implementación

    @abstractmethod
    def save(self, cliente: Cliente) -> Cliente: ...
```

### Excepciones del dominio

Son errores específicos del negocio, con su código HTTP correspondiente:

```python
# src/domain/exceptions/domain_exceptions.py
class EntityNotFoundException(DomainException):
    # Se lanza cuando buscas un cliente que no existe → HTTP 404

class DuplicateEntityException(DomainException):
    # Se lanza cuando intentas registrar un email que ya existe → HTTP 400

class InvalidCredentialsException(DomainException):
    # Se lanza cuando la contraseña es incorrecta → HTTP 401
```

---

## CAPA 2 — Application (La lógica de negocio)

```
src/application/
├── dtos/               ← Objetos para recibir y enviar datos
│   ├── auth_dto.py
│   ├── cliente_dto.py
│   ├── bodega_dto.py
│   ├── puerto_dto.py
│   └── envio_dto.py
└── use_cases/          ← Una clase por cada acción del sistema
    ├── auth/
    │   ├── register_user.py    ← Caso de uso: Registrar usuario
    │   └── login_user.py       ← Caso de uso: Iniciar sesión
    ├── clientes/
    │   ├── list_clientes.py    ← Caso de uso: Listar clientes
    │   ├── get_cliente.py      ← Caso de uso: Obtener un cliente
    │   ├── create_cliente.py   ← Caso de uso: Crear cliente
    │   ├── update_cliente.py   ← Caso de uso: Actualizar cliente
    │   └── delete_cliente.py   ← Caso de uso: Eliminar cliente
    ├── bodegas/
    ├── puertos/
    └── envios/
```

### ¿Qué es un DTO?

DTO significa **Data Transfer Object**. Es un objeto que define exactamente qué datos
se reciben o se envían en cada operación. Usa Pydantic para validar automáticamente.

```python
# src/application/dtos/cliente_dto.py

class ClienteCreateDTO(BaseModel):
    # Datos que RECIBE el servidor al crear un cliente
    nombre: str           # Obligatorio
    apellido: str         # Obligatorio
    email: EmailStr       # Obligatorio y validado como email
    telefono: str | None  # Opcional
    direccion: str | None # Opcional

class ClienteResponseDTO(BaseModel):
    # Datos que DEVUELVE el servidor
    id_cliente: int
    nombre: str
    apellido: str
    email: str
    telefono: str | None
    direccion: str | None
    created_at: datetime | None
```

### ¿Qué es un caso de uso?

Un caso de uso ejecuta **una sola acción del sistema**. Principio de Responsabilidad Única (SOLID - S).
Recibe un repositorio (el contrato) y un DTO, ejecuta la lógica y devuelve el resultado.

```python
# src/application/use_cases/clientes/create_cliente.py
class CreateClienteUseCase:
    def __init__(self, repo: ClienteRepository):  # Recibe el contrato, no la implementación
        self._repo = repo

    def execute(self, dto: ClienteCreateDTO) -> Cliente:
        # 1. Verificar que el email no esté duplicado
        if self._repo.find_by_email(dto.email):
            raise DuplicateEntityException("email", dto.email)  # → HTTP 400

        # 2. Crear la entidad
        cliente = Cliente(id_cliente=None, nombre=dto.nombre, ...)

        # 3. Guardar y retornar
        return self._repo.save(cliente)
```

---

## CAPA 3 — Infrastructure (La implementación técnica)

```
src/infrastructure/
├── database/
│   ├── connection.py        ← Conexión a PostgreSQL con SQLAlchemy
│   ├── models/              ← Mapeo de tablas de la BD a clases Python
│   │   ├── user_model.py
│   │   ├── cliente_model.py
│   │   ├── bodega_model.py
│   │   ├── puerto_model.py
│   │   ├── envio_terrestre_model.py
│   │   └── envio_maritimo_model.py
│   └── repositories/        ← Implementación concreta de los repositorios
│       ├── user_repository_impl.py
│       ├── cliente_repository_impl.py
│       ├── bodega_repository_impl.py
│       ├── puerto_repository_impl.py
│       └── envio_repository_impl.py
└── security/
    ├── jwt_service.py       ← Genera y valida tokens Bearer
    └── password_service.py  ← Encripta y verifica contraseñas
```

### Modelos de base de datos

Un modelo SQLAlchemy mapea una tabla de PostgreSQL a una clase Python.
Cuando haces una consulta, SQLAlchemy traduce tu código Python a SQL automáticamente.

```python
# src/infrastructure/database/models/cliente_model.py
class ClienteModel(Base):
    __tablename__ = "clientes"   # Nombre de la tabla en PostgreSQL

    id_cliente = Column(Integer, primary_key=True)
    nombre     = Column(String(100), nullable=False)
    apellido   = Column(String(100), nullable=False)
    email      = Column(String(150), unique=True, nullable=False)
    # ...
```

### Implementación del repositorio

Aquí es donde se "implementa" el contrato definido en Domain.
Esta clase SÍ conoce SQLAlchemy y la base de datos.

```python
# src/infrastructure/database/repositories/cliente_repository_impl.py
class ClienteRepositoryImpl(ClienteRepository):   # Implementa el contrato
    def __init__(self, db: Session):
        self._db = db

    def find_by_id(self, id_cliente: int) -> Cliente | None:
        # Consulta real a PostgreSQL
        row = self._db.query(ClienteModel).filter(ClienteModel.id_cliente == id_cliente).first()
        return self._to_entity(row) if row else None

    def save(self, cliente: Cliente) -> Cliente:
        model = ClienteModel(nombre=cliente.nombre, email=cliente.email, ...)
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    @staticmethod
    def _to_entity(m: ClienteModel) -> Cliente:
        # Convierte el modelo de BD a la entidad de dominio
        return Cliente(id_cliente=m.id_cliente, nombre=m.nombre, ...)
```

### Seguridad: JWT (Bearer Token)

Cuando el usuario hace login, el servidor genera un **token JWT** (una cadena cifrada).
Ese token se debe enviar en cada petición protegida en el header `Authorization`.

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

```python
# src/infrastructure/security/jwt_service.py
class JWTService:
    def create_token(self, payload: dict) -> str:
        # Agrega fecha de expiración y firma el token con la clave secreta
        data["exp"] = datetime.now() + timedelta(minutes=60)
        return jwt.encode(data, self._secret, algorithm="HS256")

    def decode_token(self, token: str) -> dict:
        # Verifica que el token sea válido y no haya expirado
        return jwt.decode(token, self._secret, algorithms=["HS256"])
        # Si falla → lanza UnauthorizedException → HTTP 401
```

### Seguridad: Contraseñas

Las contraseñas **NUNCA** se guardan en texto plano. Se encriptan con bcrypt.

```python
# src/infrastructure/security/password_service.py
class PasswordService:
    def hash(self, plain_password: str) -> str:
        # "admin123" → "$2b$12$abc...xyz" (irreversible)
        return bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt()).decode()

    def verify(self, plain_password: str, hashed: str) -> bool:
        # Compara "admin123" con el hash guardado sin desencriptar
        return bcrypt.checkpw(plain_password.encode(), hashed.encode())
```

---

## CAPA 4 — Presentation (Las APIs)

```
src/presentation/
├── api/
│   ├── dependencies.py     ← Inyección de dependencias de FastAPI
│   └── v1/                 ← Versión 1 de la API
│       ├── auth_router.py
│       ├── clientes_router.py
│       ├── bodegas_router.py
│       ├── puertos_router.py
│       └── envios_router.py
└── error_handlers.py       ← Manejo global de errores
```

### ¿Qué hace un Router?

Un router agrupa los endpoints de un recurso. Recibe la petición HTTP,
llama al caso de uso correspondiente y devuelve la respuesta.

```python
# src/presentation/api/v1/clientes_router.py

# dependencies=[Depends(verify_token)] → TODOS los endpoints requieren token
router = APIRouter(prefix="/clientes", tags=["Clientes"], dependencies=[Depends(verify_token)])

@router.get("/", response_model=list[ClienteResponseDTO])
def list_clientes(repo=Depends(get_cliente_repo)):
    return ListClientesUseCase(repo).execute()   # Llama al caso de uso

@router.post("/", status_code=201)
def create_cliente(dto: ClienteCreateDTO, repo=Depends(get_cliente_repo)):
    return CreateClienteUseCase(repo).execute(dto)

@router.delete("/{id_cliente}", status_code=204)
def delete_cliente(id_cliente: int, repo=Depends(get_cliente_repo)):
    DeleteClienteUseCase(repo).execute(id_cliente)
    # Si no existe → EntityNotFoundException → HTTP 404 (automático)
```

### Inyección de dependencias

FastAPI usa `Depends()` para "inyectar" dependencias automáticamente.
Esto conecta la capa Presentation con Infrastructure sin que el router lo sepa.

```python
# src/presentation/api/dependencies.py

def get_cliente_repo(db: Session = Depends(get_db)):
    return ClienteRepositoryImpl(db)   # Crea el repositorio concreto

def verify_token(credentials = Depends(HTTPBearer()), jwt = Depends(get_jwt_service)):
    return jwt.decode_token(credentials.credentials)
    # Si el token es inválido → HTTP 401 automáticamente
```

### Manejo de errores

Los errores se capturan globalmente. No necesitas try/except en cada endpoint.

```python
# src/presentation/error_handlers.py

async def domain_exception_handler(request, exc: DomainException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
    # DomainException.status_code puede ser 400, 401 o 404 según el tipo

async def validation_exception_handler(request, exc: RequestValidationError):
    # Pydantic lanza esto cuando el JSON no tiene el formato correcto → HTTP 422
    return JSONResponse(status_code=422, content={"detail": "Error de validación", "errors": [...]})

async def internal_error_handler(request, exc: Exception):
    # Cualquier error no controlado → HTTP 500
    return JSONResponse(status_code=500, content={"detail": "Error interno del servidor"})
```

---

## Códigos HTTP retornados

| Código | Nombre | ¿Cuándo ocurre? |
|--------|--------|-----------------|
| **200** | OK | Operación exitosa (GET, PUT) |
| **201** | Created | Recurso creado exitosamente (POST) |
| **204** | No Content | Eliminado correctamente (DELETE) |
| **400** | Bad Request | Email duplicado u otro error de negocio |
| **401** | Unauthorized | Token ausente, inválido o expirado |
| **404** | Not Found | El recurso solicitado no existe |
| **422** | Unprocessable Entity | Los datos enviados no tienen el formato correcto |
| **500** | Internal Server Error | Error inesperado en el servidor |

---

## Principios SOLID aplicados

| Letra | Principio | ¿Cómo se aplica? |
|-------|-----------|-----------------|
| **S** | Single Responsibility | Cada clase tiene una sola responsabilidad. `CreateClienteUseCase` solo crea clientes. |
| **O** | Open/Closed | Los DTOs usan herencia. Se pueden extender sin modificar la clase base. |
| **L** | Liskov Substitution | `ClienteRepositoryImpl` puede reemplazar a `ClienteRepository` sin romper nada. |
| **I** | Interface Segregation | Cada repositorio tiene su propia interfaz: `ClienteRepository`, `BodegaRepository`, etc. |
| **D** | Dependency Inversion | Los casos de uso dependen de la interfaz abstracta, no de la implementación concreta. |

---

## Flujo completo de una petición

Ejemplo: **Crear un cliente** (`POST /api/v1/clientes/`)

```
1. Cliente HTTP envía:
   POST /api/v1/clientes/
   Authorization: Bearer eyJhbGci...
   Body: {"nombre": "Juan", "apellido": "Pérez", "email": "juan@test.com"}

2. [Presentation] clientes_router.py
   → Verifica el token Bearer (verify_token)
   → Valida el body con Pydantic (ClienteCreateDTO)
   → Llama a CreateClienteUseCase(repo).execute(dto)

3. [Application] create_cliente.py
   → Verifica si el email ya existe: repo.find_by_email("juan@test.com")
   → Si existe → lanza DuplicateEntityException → HTTP 400
   → Crea la entidad Cliente(id=None, nombre="Juan", ...)
   → Llama a repo.save(cliente)

4. [Infrastructure] cliente_repository_impl.py
   → Convierte Cliente → ClienteModel
   → Ejecuta INSERT en PostgreSQL
   → Retorna la entidad con el ID asignado

5. [Presentation] Responde:
   HTTP 201 Created
   {"id_cliente": 6, "nombre": "Juan", "apellido": "Pérez", ...}
```

---

## Cómo correr el proyecto

### 1. Instalar dependencias
```bash
python -m pip install fastapi uvicorn sqlalchemy psycopg2-binary PyJWT "passlib[bcrypt]" python-dotenv "pydantic[email]"
```

### 2. Configurar el archivo .env
Copia `.env.example` y renómbralo a `.env`:
```env
DATABASE_URL=postgresql://postgres:TU_PASSWORD@localhost:5432/logistica_db
JWT_SECRET_KEY=una-clave-secreta-larga-y-segura
JWT_EXPIRE_MINUTES=60
```

### 3. Iniciar el servidor
```bash
cd C:\claude\logistica_backend
python main.py
```

### 4. Abrir Swagger UI
```
http://localhost:8001/docs
```

---

## Cómo usar la API desde Swagger

1. Abre `http://localhost:8001/docs`
2. Ve a **POST /api/v1/auth/register** → registra un usuario
3. Ve a **POST /api/v1/auth/login** → haz login → copia el `access_token`
4. Haz clic en el botón **Authorize** (candado arriba a la derecha)
5. Escribe: `Bearer eyJhbGci...` (pega tu token)
6. Haz clic en **Authorize** → ya puedes usar todos los endpoints protegidos

---

## Endpoints disponibles

### Autenticación (sin token)
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/auth/register` | Registrar nuevo usuario |
| POST | `/api/v1/auth/login` | Iniciar sesión → obtener token |

### Clientes (requieren token)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/clientes/` | Listar todos los clientes |
| GET | `/api/v1/clientes/{id}` | Obtener un cliente por ID |
| POST | `/api/v1/clientes/` | Crear nuevo cliente |
| PUT | `/api/v1/clientes/{id}` | Actualizar cliente |
| DELETE | `/api/v1/clientes/{id}` | Eliminar cliente |

### Bodegas (requieren token)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/bodegas/` | Listar bodegas |
| GET | `/api/v1/bodegas/{id}` | Obtener bodega |
| POST | `/api/v1/bodegas/` | Crear bodega |
| PUT | `/api/v1/bodegas/{id}` | Actualizar bodega |
| DELETE | `/api/v1/bodegas/{id}` | Eliminar bodega |

### Puertos (requieren token)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/puertos/` | Listar puertos |
| GET | `/api/v1/puertos/{id}` | Obtener puerto |
| POST | `/api/v1/puertos/` | Crear puerto |
| PUT | `/api/v1/puertos/{id}` | Actualizar puerto |
| DELETE | `/api/v1/puertos/{id}` | Eliminar puerto |

### Envíos Terrestres (requieren token)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/envios/terrestres` | Listar envíos terrestres |
| GET | `/api/v1/envios/terrestres/{id}` | Obtener envío terrestre |
| POST | `/api/v1/envios/terrestres` | Crear envío terrestre |
| PUT | `/api/v1/envios/terrestres/{id}` | Actualizar envío terrestre |
| DELETE | `/api/v1/envios/terrestres/{id}` | Eliminar envío terrestre |

### Envíos Marítimos (requieren token)
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/v1/envios/maritimos` | Listar envíos marítimos |
| GET | `/api/v1/envios/maritimos/{id}` | Obtener envío marítimo |
| POST | `/api/v1/envios/maritimos` | Crear envío marítimo |
| PUT | `/api/v1/envios/maritimos/{id}` | Actualizar envío marítimo |
| DELETE | `/api/v1/envios/maritimos/{id}` | Eliminar envío marítimo |

---

## Validaciones importantes

### Placa de camión
- Formato: `AAA123` (3 letras mayúsculas + 3 números)
- Ejemplo válido: `ABC123`
- Ejemplo inválido: `abc123`, `AB123`, `ABCD123`

### Número de flota marítima
- Formato: `AAA1234A` (3 letras + 4 números + 1 letra)
- Ejemplo válido: `FLT0001A`
- Ejemplo inválido: `FL0001A`, `FLT001A`

### Número de guía
- 10 caracteres alfanuméricos en mayúscula
- Ejemplo válido: `GT0000001A`
- Ejemplo inválido: `gt0000001a`, `GT000001` (solo 8 chars)

### Fechas
- `fecha_entrega` no puede ser anterior a `fecha_registro`

---

## Archivos del proyecto

| Archivo | Descripción |
|---------|-------------|
| `main.py` | Punto de entrada. Registra routers y manejadores de error |
| `requirements.txt` | Lista de dependencias Python |
| `.env` | Variables de entorno (no subir a Git) |
| `.env.example` | Plantilla del .env para otros desarrolladores |
| `src/domain/` | Entidades, contratos e excepciones del negocio |
| `src/application/` | DTOs y casos de uso (lógica de negocio) |
| `src/infrastructure/` | Modelos SQLAlchemy, repositorios y seguridad |
| `src/presentation/` | Routers FastAPI, dependencias y manejo de errores |
