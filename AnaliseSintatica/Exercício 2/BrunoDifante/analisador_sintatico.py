import argparse
import csv
import re
from pathlib import Path


TIPOS = {"int", "char", "float", "double", "void", "bool", "boolean",
         "short", "long", "signed", "unsigned", "if", "else", "for",
         "while", "return", "sizeof", "struct", "const"}
ABERTURA = {"(": ")", "[": "]", "{": "}"}
FECHAMENTO = set(ABERTURA.values())
SIMBOLOS = {
    "(": "AP", ")": "FP", "[": "ACOL", "]": "FCOL",
    "{": "ACH", "}": "FCH", "=": "SATR", ";": "PV", ",": "VG",
}
PADRAO_TOKEN = re.compile(
    r'//[^\n]*|/\*[\s\S]*?\*/|/\*[\s\S]*\Z|'
    r'"(?:\\[^\n]|[^"\\\n])*"' r"|'(?:\\[^\n]|[^'\\\n])*'|"
    r"^[ \t]*#[^\n]*|(?:\d+\.\d*|\.\d+)|\d+|[A-Za-z_]\w*|"
    r"==|!=|<=|>=|\+\+|--|&&|\|\||[^\s]",
    re.MULTILINE | re.ASCII,
)


def classificar(token):
    if token in TIPOS:
        return "PR:" + token.upper()
    if token in SIMBOLOS:
        return SIMBOLOS[token]
    if token.startswith("#"):
        return "PREPROCESSADOR"
    if token.startswith('"'):
        return "STRING"
    if token.startswith("'"):
        return "CARACTER"
    if token.isdecimal():
        return "INTEIRO"
    if re.fullmatch(r"\d+\.\d*|\.\d+", token):
        return "FRACIONARIO"
    if re.fullmatch(r"[A-Za-z_]\w*", token, re.ASCII):
        return "NOMEVARIAVEL"
    return "SIMBOLO"


def analisar(texto):
    tabela, pilha, erros = [], [], []
    linha, inicio_linha, fim_anterior = 1, 0, 0
    for trecho in PADRAO_TOKEN.finditer(texto):
        posicao = trecho.start()
        linha += texto.count("\n", fim_anterior, posicao)
        quebra = texto.rfind("\n", fim_anterior, posicao)
        if quebra != -1:
            inicio_linha = quebra + 1
        fim_anterior = posicao
        token = trecho.group()
        if token.startswith(("//", "/*")):
            if token.startswith("/*") and not token[2:].endswith("*/"):
                erros.append(f"Linha {linha}: comentário de bloco sem fechamento.")
            continue
        token = token.lstrip()
        coluna = posicao - inicio_linha + 1 + len(trecho.group()) - len(token)
        identificador = len(tabela) + 1
        referencia = ""
        if token in ABERTURA:
            pilha.append((token, identificador, linha, coluna))
        elif token in FECHAMENTO:
            if not pilha:
                erros.append(f"Linha {linha}, coluna {coluna}: {token} sem abertura.")
            elif ABERTURA[pilha[-1][0]] != token:
                esperado = ABERTURA[pilha[-1][0]]
                erros.append(f"Linha {linha}, coluna {coluna}: esperado {esperado}, encontrado {token}.")
            else:
                _, referencia, _, _ = pilha.pop()
        tabela.append((identificador, token, classificar(token), linha, coluna, referencia))

    for token, _, linha, coluna in reversed(pilha):
        erros.append(f"Linha {linha}, coluna {coluna}: {token} sem fechamento.")
    return tabela, erros


def main():
    pasta = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Verifica o balanceamento de delimitadores em C.")
    parser.add_argument("entrada", type=Path, nargs="?", default=pasta / "input.c")
    parser.add_argument("--saida", type=Path, default=pasta / "tabela_simbolos.csv")
    args = parser.parse_args()
    tabela, erros = analisar(args.entrada.read_text(encoding="utf-8-sig"))
    with args.saida.open("w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.writer(arquivo, delimiter=";", lineterminator="\n")
        escritor.writerow(("ID", "token", "tipo", "linha", "coluna", "Ref"))
        escritor.writerows(tabela)
    if erros:
        print("\n".join(erros))
        return 1
    print("Delimitadores balanceados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
