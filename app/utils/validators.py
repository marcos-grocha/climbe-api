from __future__ import annotations

import re

from app.exceptions import CnpjInvalidoError, CpfInvalidoError


def validar_cpf(cpf: str) -> str:
    """Normaliza para 11 dígitos e valida os dígitos verificadores.

    Retorna o CPF só com dígitos. Levanta `CpfInvalidoError` se for inválido.
    """
    digitos = re.sub(r"\D", "", cpf)
    if len(digitos) != 11 or digitos == digitos[0] * 11:
        raise CpfInvalidoError
    for i in (9, 10):
        soma = sum(int(digitos[j]) * ((i + 1) - j) for j in range(i))
        verificador = (soma * 10) % 11 % 10
        if verificador != int(digitos[i]):
            raise CpfInvalidoError
    return digitos


def validar_cnpj(cnpj: str) -> str:
    """Normaliza para 14 dígitos e valida os dígitos verificadores.

    Retorna o CNPJ só com dígitos. Levanta `CnpjInvalidoError` se for inválido.
    """
    digitos = re.sub(r"\D", "", cnpj)
    if len(digitos) != 14 or digitos == digitos[0] * 14:
        raise CnpjInvalidoError
    pesos_primeiro = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_segundo = [6, *pesos_primeiro]
    for pesos, pos in ((pesos_primeiro, 12), (pesos_segundo, 13)):
        soma = sum(int(digitos[i]) * pesos[i] for i in range(pos))
        resto = soma % 11
        verificador = 0 if resto < 2 else 11 - resto
        if verificador != int(digitos[pos]):
            raise CnpjInvalidoError
    return digitos
