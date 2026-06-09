from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.exceptions import AppError
from app.routers import (
    auth,
    cargos,
    contratos,
    empresas,
    health,
    propostas,
    servicos,
    usuarios,
)

app = FastAPI(title="Climbe API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppError)
async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
    """Converte erros de aplicação no padrão `{detail, code}`."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "code": exc.code},
    )


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(cargos.router)
app.include_router(usuarios.router)
app.include_router(servicos.router)
app.include_router(empresas.router)
app.include_router(propostas.router)
app.include_router(contratos.router)
