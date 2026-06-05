from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models import Servico
from app.schemas.servico import ServicoResponse
from app.services import servico_service

router = APIRouter(prefix="/servicos", tags=["servicos"])


@router.get("", response_model=list[ServicoResponse], dependencies=[Depends(get_current_user)])
def listar(db: Annotated[Session, Depends(get_db)]) -> list[Servico]:
    return servico_service.listar_servicos(db)
