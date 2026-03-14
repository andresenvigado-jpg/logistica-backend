import sys
import os
_base = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _base)
os.chdir(_base)

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.database.connection import engine
from src.infrastructure.database.models import user_model, cliente_model, bodega_model, puerto_model
from src.infrastructure.database.models import envio_terrestre_model, envio_maritimo_model
from src.infrastructure.database.connection import Base

from src.presentation.api.v1.auth_router import router as auth_router
from src.presentation.api.v1.clientes_router import router as clientes_router
from src.presentation.api.v1.bodegas_router import router as bodegas_router
from src.presentation.api.v1.puertos_router import router as puertos_router
from src.presentation.api.v1.envios_router import router as envios_router

from src.presentation.error_handlers import (
    domain_exception_handler, validation_exception_handler, internal_error_handler
)
from src.domain.exceptions.domain_exceptions import DomainException

# Crear tablas nuevas (solo usuarios; las demás ya existen)
Base.metadata.create_all(bind=engine, tables=[user_model.UserModel.__table__])

app = FastAPI(
    title="API Gestión Logística",
    description="Sistema de gestión de envíos terrestres y marítimos. Requiere autenticación Bearer.",
    version="1.0.0",
    contact={"name": "Logística SAS"},
)

# CORS - Permite peticiones desde el frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manejadores de errores globales
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, internal_error_handler)

# Routers
PREFIX = "/api/v1"
app.include_router(auth_router, prefix=PREFIX)
app.include_router(clientes_router, prefix=PREFIX)
app.include_router(bodegas_router, prefix=PREFIX)
app.include_router(puertos_router, prefix=PREFIX)
app.include_router(envios_router, prefix=PREFIX)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=False)
