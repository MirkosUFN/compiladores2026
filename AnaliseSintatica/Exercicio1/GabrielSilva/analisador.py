import csv
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

TIPOS = {
    "int": "PR:INT", "char": "PR:CHAR", "float": "PR:FLOAT",
    "double": "PR:DOUBLE", "void": "PR:VOID", "boolean": "PR:BOOLEAN",
}

VALORES_BOOLEANOS = {"true": "PR:TRUE", "false": "PR:FALSE"}
TIPOS_DE_VALOR = {"INTEIRO", "FRACIONARIO", "NOMEVARIAVEL", "PR:TRUE", "PR:FALSE"}

PADRAO_TOKEN = re.compile(
    r"[+-]?(?:\d+\.\d+|\.\d+)|[+-]?\d+|[A-Za-z_][A-Za-z0-9_]*|==|<=|>=|!=|[,;=<>!]|[^\s]"
)

@dataclass
class Token:
    lexema: str
    tipo: str
    linha: int
    coluna: int
    aceito: bool = True

@dataclass
class Declarador:
    nome: str
    valor: Optional[str] = None

@dataclass
class ResultadoSintatico:
    aceito: bool
    tipo: Optional[str]
    declaradores: List[Declarador]
    mensagem: str

def classificar_lexema(lexema: str) -> Tuple[str, bool]:
    if lexema in TIPOS: return TIPOS[lexema], True
    if lexema in VALORES_BOOLEANOS: return VALORES_BOOLEANOS[lexema], True
    if re.fullmatch(r"[+-]?\d+", lexema): return "INTEIRO", True
    if re.fullmatch(r"[+-]?(?:\d+\.\d+|\.\d+)", lexema): return "FRACIONARIO", True
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", lexema): return "NOMEVARIAVEL", True
    if lexema == "=": return "ATRIBUICAO", True
    if lexema == ",": return "VIRGULA", True
    if lexema == ";": return "PONTO_VIRGULA", True
    return "NAO_RECONHECIDO", False

def tokenizar_linha(linha: str, numero_linha: int) -> List[Token]:
    tokens = []
    for correspondencia in PADRAO_TOKEN.finditer(linha):
        lexema = correspondencia.group(0)
        tipo, aceito = classificar_lexema(lexema)
        tokens.append(Token(lexema, tipo, numero_linha, correspondencia.start() + 1, aceito))
    return tokens

def analisar_declaracao(tokens: List[Token]) -> ResultadoSintatico:
    if not tokens:
        return ResultadoSintatico(False, None, [], "Linha vazia.")

    tipo = tokens[0].tipo
    if tipo not in TIPOS.values():
        return ResultadoSintatico(False, None, [], "A linha não começa com um TIPO válido.")

    indice = 1
    declaradores: List[Declarador] = []

    while True:
        if indice >= len(tokens) or tokens[indice].tipo != "NOMEVARIAVEL":
            encontrado = tokens[indice].lexema if indice < len(tokens) else "fim da linha"
            return ResultadoSintatico(False, tipo, declaradores, f"Era esperado NOMEVARIAVEL, mas foi encontrado '{encontrado}'.")

        nome = tokens[indice].lexema
        indice += 1
        valor: Optional[str] = None

        if indice < len(tokens) and tokens[indice].tipo == "ATRIBUICAO":
            indice += 1
            if indice >= len(tokens) or tokens[indice].tipo not in TIPOS_DE_VALOR:
                encontrado = tokens[indice].lexema if indice < len(tokens) else "fim da linha"
                return ResultadoSintatico(False, tipo, declaradores, f"Era esperado VALOR depois de '=' para '{nome}', mas foi encontrado '{encontrado}'.")
            
            valor = tokens[indice].lexema
            indice += 1

        declaradores.append(Declarador(nome=nome, valor=valor))

        if indice >= len(tokens):
            return ResultadoSintatico(False, tipo, declaradores, "Era esperado PONTO_VIRGULA ao final da declaração.")

        if tokens[indice].tipo == "VIRGULA":
            indice += 1
            continue
        break

    if tokens[indice].tipo != "PONTO_VIRGULA":
        return ResultadoSintatico(False, tipo, declaradores, f"Era esperado PONTO_VIRGULA, mas foi encontrado '{tokens[indice].lexema}'.")

    if indice != len(tokens) - 1:
        encontrado = tokens[indice + 1].lexema
        return ResultadoSintatico(False, tipo, declaradores, f"Token inesperado depois de PONTO_VIRGULA: '{encontrado}'.")

    return ResultadoSintatico(True, tipo, declaradores, f"Declaração aceita com {len(declaradores)} variável(is) e {sum(item.valor is not None for item in declaradores)} inicialização(ões).")

def criar_tabela_simbolos(caminho_csv: str) -> None:
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow(["ID", "token", "tipo", "linha", "coluna"])

def adicionar_simbolo(caminho_csv: str, identificador: int, token: Token) -> None:
    with open(caminho_csv, "a", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow([identificador, token.lexema, token.tipo, token.linha, token.coluna])

def processar_arquivo(caminho_entrada: str, caminho_csv: str) -> None:
    criar_tabela_simbolos(caminho_csv)
    proximo_id = 1

    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            tokens = tokenizar_linha(linha, numero_linha)
            if not tokens: continue

            print(f"\nLinha {numero_linha}: {linha.rstrip()}")
            for token in tokens:
                if token.aceito:
                    adicionar_simbolo(caminho_csv, proximo_id, token)
                    proximo_id += 1

            resultado = analisar_declaracao(tokens)
            status = "ACEITA" if resultado.aceito else "REJEITADA"
            print(f"  [DECLARACAO {status}]")
            print(f"  Mensagem: {resultado.mensagem}")

def main() -> None:
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_entrada = os.path.join(diretorio, "input.c")
    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")

    if not os.path.exists(caminho_entrada):
        print(f"Ficheiro de entrada não encontrado: {caminho_entrada}")
        return

    processar_arquivo(caminho_entrada, caminho_csv)
    print(f"\nTabela de símbolos salva em: {caminho_csv}")

if __name__ == "__main__":
    main()