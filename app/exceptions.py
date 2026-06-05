from __future__ import annotations

from fastapi import status


class AppError(Exception):
    """Erro de aplicação com status HTTP e código estável (padrão `{detail, code}`)."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "ERRO"
    detail: str = "Erro inesperado"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class CredenciaisInvalidasError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "AUTH_CREDENCIAIS_INVALIDAS"
    detail = "Email ou senha inválidos"


class TokenInvalidoError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "AUTH_TOKEN_INVALIDO"
    detail = "Token inválido ou expirado"


class UsuarioInativoError(AppError):
    status_code = status.HTTP_401_UNAUTHORIZED
    code = "AUTH_USUARIO_INATIVO"
    detail = "Usuário inativo"


class SemPermissaoError(AppError):
    status_code = status.HTTP_403_FORBIDDEN
    code = "AUTH_SEM_PERMISSAO"
    detail = "Você não tem permissão para esta ação"
