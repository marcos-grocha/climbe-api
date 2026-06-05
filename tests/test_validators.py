from __future__ import annotations

import pytest

from app.exceptions import CpfInvalidoError
from app.utils.validators import validar_cpf


def test_cpf_valido_normaliza() -> None:
    assert validar_cpf("529.982.247-25") == "52998224725"


def test_cpf_digito_verificador_errado() -> None:
    with pytest.raises(CpfInvalidoError):
        validar_cpf("529.982.247-20")


def test_cpf_sequencia_trivial() -> None:
    with pytest.raises(CpfInvalidoError):
        validar_cpf("111.111.111-11")


def test_cpf_tamanho_errado() -> None:
    with pytest.raises(CpfInvalidoError):
        validar_cpf("123")
