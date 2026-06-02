from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Base declarativa da qual todos os models herdam."""


def get_db() -> Generator[Session, None, None]:
    """Dependency do FastAPI: abre uma sessão e a fecha ao fim da request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
