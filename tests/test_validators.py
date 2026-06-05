from __future__ import annotations

import pytest

from app.exceptions import CnpjInvalidoError, CpfInvalidoError
from app.utils.validators import validar_cnpj, validar_cpf


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


def test_cnpj_valido_normaliza() -> None:
    assert validar_cnpj("11.222.333/0001-81") == "11222333000181"


def test_cnpj_digito_verificador_errado() -> None:
    with pytest.raises(CnpjInvalidoError):
        validar_cnpj("11.222.333/0001-80")


def test_cnpj_sequencia_trivial() -> None:
    with pytest.raises(CnpjInvalidoError):
        validar_cnpj("00000000000000")


def test_cnpj_tamanho_errado() -> None:
    with pytest.raises(CnpjInvalidoError):
        validar_cnpj("123")
