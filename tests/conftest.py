from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.database import engine
from app.main import app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_session() -> Iterator[Session]:
    """Sessão de teste isolada: cada teste roda numa transação revertida ao fim."""
    connection = engine.connect()
    transaction = connection.begin()
    # create_savepoint: um flush que falha (ex.: IntegrityError) reverte apenas o
    # savepoint, mantendo a transação externa viva para o rollback final.
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()
