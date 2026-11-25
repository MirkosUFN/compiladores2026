import csv
import os
import re
import sys
from dataclasses import dataclass
from typing import Dict, List, Optional

PALAVRAS_RESERVADAS = {
    "int": "PR:INT",
    "char": "PR:CHAR",
    "float": "PR:FLOAT",
    "double": "PR:DOUBLE",
    "void": "PR:VOID",
    "boolean": "PR:BOOLEAN",
    "bool": "PR:BOOLEAN",
    "if": "PR:IF",
    "else": "PR:ELSE",
    "for": "PR:FOR",
    "while": "PR:WHILE",
    "return": "PR:RETURN",
    "true": "PR:TRUE",
    "false": "PR:FALSE",
}

# Símbolos de agrupamento
ABRE = {"(": "AP", "{": "ACH", "[": "ACO"}
FECHA = {")": "FP", "}": "FCH", "]": "FCO"}
PAR_DE = {")": "(", "}": "{", "]": "["}

OPERADORES = {
    "==": "SINAL_COMPARACAO", "!=": "SINAL_COMPARACAO",
    "<=": "SINAL_COMPARACAO", ">=": "SINAL_COMPARACAO",
    "<": "SINAL_COMPARACAO", ">": "SINAL_COMPARACAO",
    "&&": "E_LOGICO", "||": "OU_LOGICO", "!": "NAO_LOGICO",
    "++": "INCREMENTO", "--": "DECREMENTO",
    "=": "SATR",
    "+": "SOMA", "-": "SUB", "*": "MULT", "/": "DIV", "%": "MOD",
    ",": "VG", ";": "PV",
}

PADRAO_TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"'            # texto
    r"|'(?:\\.|[^'\\])'"            # caractere
    r"|\d+\.\d+"                    # fracionário
    r"|\d+"                         # inteiro
    r"|[A-Za-z_][A-Za-z0-9_]*"      # identificador / palavra reservada
    r"|==|!=|<=|>=|&&|\|\||\+\+|--" # operadores compostos
    r"|[(){}\[\]<>=!+\-*/%,;]"      # operadores simples e delimitadores
    r"|\S"                          # qualquer outro caractere
)


@dataclass
class Token:
    id: int
    lexema: str
    tipo: str
    linha: int
    coluna: int
    ref: Optional[int] = None


@dataclass
class ErroSintatico:
    linha: int
    coluna: int
    mensagem: str


def classificar(lexema: str) -> str:
    if lexema in PALAVRAS_RESERVADAS:
        return PALAVRAS_RESERVADAS[lexema]
    if lexema in ABRE:
        return ABRE[lexema]
    if lexema in FECHA:
        return FECHA[lexema]
    if lexema in OPERADORES:
        return OPERADORES[lexema]
    if re.fullmatch(r"\d+\.\d+", lexema):
        return "FRACIONARIO"
    if re.fullmatch(r"\d+", lexema):
        return "INTEIRO"
    if lexema.startswith('"'):
        return "TEXTO"
    if lexema.startswith("'"):
        return "CARACTERE"
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", lexema):
        return "NOMEVARIAVEL"
    return "NAO_RECONHECIDO"


def tokenizar(caminho: str) -> List[Token]:
    tokens: List[Token] = []
    with open(caminho, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            for encontrado in PADRAO_TOKEN.finditer(linha.expandtabs(4)):
                lexema = encontrado.group(0)
                tokens.append(Token(
                    id=len(tokens) + 1,
                    lexema=lexema,
                    tipo=classificar(lexema),
                    linha=numero_linha,
                    coluna=encontrado.start() + 1,
                ))
    return tokens


def verificar_balanceamento(tokens: List[Token]) -> List[ErroSintatico]:
    """
    Percorre os tokens usando uma pilha:
      - token de abertura -> empilha
      - token de fechamento -> desempilha e confere se é do mesmo tipo;
        se for, grava o ID do abre na coluna Ref do fecha
    Ao final, o que sobrar na pilha são aberturas sem fechamento.
    """
    pilha: List[Token] = []
    erros: List[ErroSintatico] = []

    for token in tokens:
        if token.lexema in ABRE:
            pilha.append(token)

        elif token.lexema in FECHA:
            esperado = PAR_DE[token.lexema]
            if not pilha:
                erros.append(ErroSintatico(
                    token.linha, token.coluna,
                    f"'{token.lexema}' (ID {token.id}) fecha algo que não foi aberto."))
                continue

            topo = pilha[-1]
            if topo.lexema == esperado:
                pilha.pop()
                token.ref = topo.id
            else:
                erros.append(ErroSintatico(
                    token.linha, token.coluna,
                    f"'{token.lexema}' (ID {token.id}) encontrado, mas o último aberto foi "
                    f"'{topo.lexema}' (ID {topo.id}, linha {topo.linha}, coluna {topo.coluna})."))
                # O fecha errado é descartado (fica sem Ref) e a pilha não é alterada

    for aberto in pilha:
        erros.append(ErroSintatico(
            aberto.linha, aberto.coluna,
            f"'{aberto.lexema}' (ID {aberto.id}) não foi fechado."))

    return erros


def contar_pares(tokens: List[Token]) -> Dict[str, List[int]]:
    contagem = {"( )": [0, 0], "{ }": [0, 0], "[ ]": [0, 0]}
    for token in tokens:
        for chave in contagem:
            if token.lexema == chave[0]:
                contagem[chave][0] += 1
            elif token.lexema == chave[2]:
                contagem[chave][1] += 1
    return contagem


def salvar_tabela(tokens: List[Token], caminho_csv: str) -> None:
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
        tabela = csv.writer(arquivo, delimiter=";", lineterminator="\n")
        tabela.writerow(["ID", "Token", "Tipo", "Linha", "Coluna", "Ref"])
        for token in tokens:
            tabela.writerow([token.id, token.lexema, token.tipo, token.linha, token.coluna,
                             token.ref if token.ref is not None else ""])


def main() -> None:
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_entrada = sys.argv[1] if len(sys.argv) > 1 else os.path.join(diretorio, "input.c")
    nome_base = os.path.splitext(os.path.basename(caminho_entrada))[0]
    sufixo = "" if nome_base == "input" else f"_{nome_base}"
    caminho_csv = os.path.join(diretorio, f"tabela_simbolos{sufixo}.csv")

    tokens = tokenizar(caminho_entrada)
    erros = verificar_balanceamento(tokens)
    salvar_tabela(tokens, caminho_csv)

    print(f"Arquivo analisado: {caminho_entrada}\n")
    print("Contagem de abre / fecha:")
    for par, (abertos, fechados) in contar_pares(tokens).items():
        situacao = "OK" if abertos == fechados else "DIFERENTE"
        print(f"  {par}: {abertos} abre, {fechados} fecha -> {situacao}")

    print("\nPares encontrados (fecha -> Ref):")
    por_id = {t.id: t for t in tokens}
    for token in tokens:
        if token.ref is not None:
            aberto = por_id[token.ref]
            print(f"  ID {token.id:>3} '{token.lexema}' (L{token.linha}:C{token.coluna}) "
                  f"-> ID {aberto.id:>3} '{aberto.lexema}' (L{aberto.linha}:C{aberto.coluna})")

    if erros:
        print(f"\nERRO: {len(erros)} problema(s) de balanceamento:")
        for erro in sorted(erros, key=lambda e: (e.linha, e.coluna)):
            print(f"  Linha {erro.linha}, coluna {erro.coluna}: {erro.mensagem}")
        print("\nResultado: SINTAXE REJEITADA")
    else:
        print("\nResultado: SINTAXE ACEITA (todos os ( ), { } e [ ] estão balanceados)")

    print(f"Tabela de símbolos salva em: {caminho_csv}")


if __name__ == "__main__":
    main()
