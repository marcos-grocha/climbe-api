from __future__ import annotations

import re

from app.exceptions import CpfInvalidoError


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
