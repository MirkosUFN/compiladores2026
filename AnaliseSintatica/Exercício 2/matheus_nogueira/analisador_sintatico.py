import csv
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple


TIPOS = {
    "int": "PR:INT",
    "char": "PR:CHAR",
    "float": "PR:FLOAT",
    "double": "PR:DOUBLE",
    "void": "PR:VOID",
    "boolean": "PR:BOOLEAN",
}

VALORES_BOOLEANOS = {
    "true": "PR:TRUE",
    "false": "PR:FALSE",
}

DELIMITADORES_ABERTURA = {
    "(": "ABRE_PARENTESE",
    "{": "ABRE_CHAVE",
    "[": "ABRE_COLCHETE",
}

DELIMITADORES_FECHAMENTO = {
    ")": "FECHA_PARENTESE",
    "}": "FECHA_CHAVE",
    "]": "FECHA_COLCHETE",
}

PARES_DELIMITADORES = {
    ")": "(",
    "}": "{",
    "]": "[",
}

TIPOS_DE_DELIMITADOR = {
    **DELIMITADORES_ABERTURA,
    **DELIMITADORES_FECHAMENTO,
}

PADRAO_TOKEN = re.compile(
    r"[+-]?(?:\d+\.\d+|\.\d+)|[+-]?\d+|"
    r"[A-Za-z_][A-Za-z0-9_]*|==|<=|>=|!=|"
    r"[()\[\]{},;=+\-*/<>]|[^\s]"
)


@dataclass
class Token:
    """Token reconhecido, com posição e referência na tabela de símbolos."""

    lexema: str
    tipo: str
    linha: int
    coluna: int
    aceito: bool = True
    identificador: Optional[int] = None
    ref: Optional[int] = None


@dataclass
class ResultadoDelimitadores:
    """Resultado da validação dos delimitadores do arquivo."""

    aceito: bool
    mensagem: str
    pares: int


def classificar_lexema(lexema: str) -> Tuple[str, bool]:
    """Classifica um lexema nos terminais utilizados pelo exercício."""
    if lexema in TIPOS:
        return TIPOS[lexema], True

    if lexema in VALORES_BOOLEANOS:
        return VALORES_BOOLEANOS[lexema], True

    if re.fullmatch(r"[+-]?\d+", lexema):
        return "INTEIRO", True

    if re.fullmatch(r"[+-]?(?:\d+\.\d+|\.\d+)", lexema):
        return "FRACIONARIO", True

    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", lexema):
        return "NOMEVARIAVEL", True

    if lexema in DELIMITADORES_ABERTURA:
        return DELIMITADORES_ABERTURA[lexema], True

    if lexema in DELIMITADORES_FECHAMENTO:
        return DELIMITADORES_FECHAMENTO[lexema], True

    if lexema == "=":
        return "ATRIBUICAO", True

    if lexema == ",":
        return "VIRGULA", True

    if lexema == ";":
        return "PONTO_VIRGULA", True

    if lexema in {"+", "-", "*", "/", "<", ">", "==", "<=", ">=", "!="}:
        return "OPERADOR", True

    return "NAO_RECONHECIDO", False


def tokenizar_linha(linha: str, numero_linha: int) -> List[Token]:
    """Tokeniza uma linha e registra a posição original de cada lexema."""
    tokens = []

    for correspondencia in PADRAO_TOKEN.finditer(linha):
        lexema = correspondencia.group(0)
        tipo, aceito = classificar_lexema(lexema)
        tokens.append(
            Token(
                lexema=lexema,
                tipo=tipo,
                linha=numero_linha,
                coluna=correspondencia.start() + 1,
                aceito=aceito,
            )
        )

    return tokens


def atribuir_identificadores(linhas: List[List[Token]]) -> int:
    """Atribui IDs sequenciais aos tokens aceitos da tabela de símbolos."""
    proximo_id = 1

    for tokens in linhas:
        for token in tokens:
            if token.aceito:
                token.identificador = proximo_id
                proximo_id += 1

    return proximo_id


def analisar_delimitadores(tokens: List[Token]) -> ResultadoDelimitadores:
    """
    Valida quantidade, ordem e tipo dos delimitadores.

    A pilha guarda o token de abertura. Quando o fechamento correspondente é
    encontrado, seu campo ``ref`` recebe o ID do token de abertura.
    """
    pilha: List[Token] = []
    pares = 0

    for token in tokens:
        if not token.aceito:
            continue

        if token.lexema in DELIMITADORES_ABERTURA:
            pilha.append(token)
            continue

        if token.lexema not in DELIMITADORES_FECHAMENTO:
            continue

        if not pilha:
            return ResultadoDelimitadores(
                aceito=False,
                mensagem=(
                    f"Fechamento '{token.lexema}' sem abertura correspondente "
                    f"(linha {token.linha}, coluna {token.coluna})."
                ),
                pares=pares,
            )

        abertura = pilha[-1]
        esperado = PARES_DELIMITADORES[token.lexema]

        if abertura.lexema != esperado:
            return ResultadoDelimitadores(
                aceito=False,
                mensagem=(
                    f"Fechamento '{token.lexema}' não corresponde à abertura "
                    f"'{abertura.lexema}' do token {abertura.identificador}. "
                    f"(linha {token.linha}, coluna {token.coluna})."
                ),
                pares=pares,
            )

        pilha.pop()
        token.ref = abertura.identificador
        pares += 1

    if pilha:
        abertura = pilha[-1]
        return ResultadoDelimitadores(
            aceito=False,
            mensagem=(
                f"Abertura '{abertura.lexema}' do token {abertura.identificador} "
                "não possui fechamento correspondente."
            ),
            pares=pares,
        )

    return ResultadoDelimitadores(
        aceito=True,
        mensagem=f"Delimitadores balanceados: {pares} par(es) validado(s).",
        pares=pares,
    )


def criar_tabela_simbolos(caminho_csv: str) -> None:
    """Cria a tabela com a coluna Ref solicitada no enunciado."""
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow(
            ["ID", "token", "tipo", "linha", "coluna", "Ref"]
        )


def adicionar_simbolo(caminho_csv: str, token: Token) -> None:
    """Adiciona um token aceito à tabela de símbolos."""
    with open(caminho_csv, "a", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow(
            [
                token.identificador,
                token.lexema,
                token.tipo,
                token.linha,
                token.coluna,
                token.ref if token.ref is not None else "",
            ]
        )


def mostrar_tokens(tokens: List[Token]) -> None:
    """Exibe no terminal os tokens encontrados em uma linha."""
    for token in tokens:
        status = "ACEITO" if token.aceito else "REJEITADO"
        print(
            f"  [{status}] {token.lexema!r} -> {token.tipo} "
            f"(linha {token.linha}, coluna {token.coluna})"
        )


def processar_arquivo(caminho_entrada: str, caminho_csv: str) -> None:
    """Lê o arquivo, valida delimitadores e gera a tabela de símbolos."""
    linhas: List[List[Token]] = []

    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            tokens = tokenizar_linha(linha, numero_linha)
            linhas.append(tokens)

            if tokens:
                print(f"\nLinha {numero_linha}: {linha.rstrip()}")
                mostrar_tokens(tokens)

    total_tokens = atribuir_identificadores(linhas)
    tokens = [token for linha in linhas for token in linha]
    resultado = analisar_delimitadores(tokens)

    criar_tabela_simbolos(caminho_csv)
    for token in tokens:
        if token.aceito:
            adicionar_simbolo(caminho_csv, token)

    status = "ACEITA" if resultado.aceito else "REJEITADA"
    print(f"\n[ANALISE DE DELIMITADORES {status}]")
    print(f"  {resultado.mensagem}")

    if total_tokens > 1:
        print(f"  Tokens aceitos: {total_tokens - 1}")


def main() -> None:
    """Executa a análise do input.c e gera a tabela de símbolos."""
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_entrada = os.path.join(diretorio, "input.c")
    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")

    if not os.path.exists(caminho_entrada):
        raise FileNotFoundError(
            f"Arquivo de entrada não encontrado: {caminho_entrada}"
        )

    print("=" * 67)
    print(" ANALISADOR SINTATICO - DELIMITADORES")
    print("=" * 67)
    processar_arquivo(caminho_entrada, caminho_csv)
    print(f"\nTabela de símbolos salva em:\n{caminho_csv}")


if __name__ == "__main__":
    main()
