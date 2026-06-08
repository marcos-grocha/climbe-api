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


class CpfInvalidoError(AppError):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    code = "CPF_INVALIDO"
    detail = "CPF inválido"


class EmailDuplicadoError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "USUARIO_EMAIL_DUPLICADO"
    detail = "Já existe um usuário com este email"


class CpfDuplicadoError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "USUARIO_CPF_DUPLICADO"
    detail = "Já existe um usuário com este CPF"


class UsuarioNaoEncontradoError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "USUARIO_NAO_ENCONTRADO"
    detail = "Usuário não encontrado"


class CargoNaoEncontradoError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "CARGO_NAO_ENCONTRADO"
    detail = "Cargo não encontrado"


class CargoEmUsoError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "CARGO_EM_USO"
    detail = "Cargo está em uso por algum usuário"


class SenhaAtualIncorretaError(AppError):
    status_code = status.HTTP_400_BAD_REQUEST
    code = "SENHA_ATUAL_INCORRETA"
    detail = "Senha atual incorreta"


class CnpjInvalidoError(AppError):
    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    code = "CNPJ_INVALIDO"
    detail = "CNPJ inválido"


class CnpjDuplicadoError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "EMPRESA_CNPJ_DUPLICADO"
    detail = "Já existe uma empresa com este CNPJ"


class EmpresaNaoEncontradaError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "EMPRESA_NAO_ENCONTRADA"
    detail = "Empresa não encontrada"


class EmpresaComVinculosError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "EMPRESA_COM_VINCULOS"
    detail = "Empresa não pode ser removida porque possui propostas vinculadas"


class ServicoNaoEncontradoError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "SERVICO_NAO_ENCONTRADO"
    detail = "Serviço não encontrado"


class PropostaNaoEncontradaError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "PROPOSTA_NAO_ENCONTRADA"
    detail = "Proposta não encontrada"


class PropostaTransicaoInvalidaError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "PROPOSTA_TRANSICAO_INVALIDA"
    detail = "Transição de status inválida para a proposta"


class PropostaComContratoError(AppError):
    status_code = status.HTTP_409_CONFLICT
    code = "PROPOSTA_COM_CONTRATO"
    detail = "Proposta não pode ser removida porque já possui contrato"
