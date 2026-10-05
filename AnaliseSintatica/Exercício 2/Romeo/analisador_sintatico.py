"""
Analisador Sintático - balanceamento de ( ), { } e [ ] - Romeo Noro Guterres

Etapas:
  1. Léxico: transforma o arquivo .c em uma lista de tokens (tipo, lexema,
     linha, coluna).
  2. Sintático: percorre os tokens com uma pilha. Cada token de abertura é
     empilhado; cada token de fechamento desempilha a abertura do topo e
     confere se é do mesmo tipo. O fechamento guarda em Ref o ID da abertura
     correspondente.
  3. Ao final, a quantidade de aberturas e fechamentos de cada delimitador é
     comparada (o enunciado exige contagem idêntica) e a tabela de símbolos é
     gravada com a coluna Ref.

Uso: python analisador_sintatico.py [arquivo.c]
     (a tabela é gravada como tabela_simbolos.csv para input.c e como
      tabela_simbolos_<arquivo>.csv para qualquer outra entrada)
"""
import csv
import os
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))

PALAVRAS_RESERVADAS = {
    "int": "PR:INT", "char": "PR:CHAR", "float": "PR:FLOAT",
    "double": "PR:DOUBLE", "void": "PR:VOID", "boolean": "PR:BOOLEAN",
    "true": "PR:TRUE", "false": "PR:FALSE", "if": "PR:IF", "else": "PR:ELSE",
    "while": "PR:WHILE", "for": "PR:FOR", "return": "PR:RETURN",
}

# delimitadores: lexema -> tipo do token
ABERTURAS = {"(": "AP", "{": "ACH", "[": "ACO"}
FECHAMENTOS = {")": "FP", "}": "FCH", "]": "FCO"}
PAR_DE = {"FP": "AP", "FCH": "ACH", "FCO": "ACO"}   # fechamento -> abertura
NOME = {"AP": "parêntese", "ACH": "chave", "ACO": "colchete"}

OPERADORES_DUPLOS = {"==": "IGUAL", "!=": "DIFERENTE", ">=": "MAIORIGUAL",
                     "<=": "MENORIGUAL", "&&": "E", "||": "OU",
                     "++": "INCREMENTO", "--": "DECREMENTO"}
SIMBOLOS = {"=": "SATR", ",": "VG", ";": "PV", ">": "MAIOR", "<": "MENOR",
            "+": "SOMA", "-": "SUB", "*": "MULT", "/": "DIV", "!": "NAO",
            **ABERTURAS, **FECHAMENTOS}


# ----------------------------------------------------------------- léxico

class Token:
    def __init__(self, id_, tipo, lexema, linha, coluna):
        self.id, self.tipo, self.lexema = id_, tipo, lexema
        self.linha, self.coluna = linha, coluna
        self.ref = None   # só preenchido nos tokens de fechamento

    def __repr__(self):
        return f"{self.tipo}({self.lexema!r}) {self.linha}:{self.coluna}"


def analisar_lexico(fonte):
    tokens = []

    def novo(tipo, lexema, linha, coluna):
        tokens.append(Token(len(tokens) + 1, tipo, lexema, linha, coluna))

    for num_linha, linha in enumerate(fonte.splitlines(), start=1):
        i, n = 0, len(linha)
        while i < n:
            c = linha[i]
            col = i + 1

            if c.isspace():
                i += 1

            elif linha.startswith("//", i):
                break

            elif c.isalpha() or c == "_":
                j = i
                while j < n and (linha[j].isalnum() or linha[j] == "_"):
                    j += 1
                palavra = linha[i:j]
                novo(PALAVRAS_RESERVADAS.get(palavra, "NOMEVARIAVEL"), palavra, num_linha, col)
                i = j

            elif c.isdigit():
                j = i
                while j < n and linha[j].isdigit():
                    j += 1
                tipo = "INTEIRO"
                if j + 1 < n and linha[j] == "." and linha[j + 1].isdigit():
                    j += 1
                    while j < n and linha[j].isdigit():
                        j += 1
                    tipo = "FRACIONARIO"
                novo(tipo, linha[i:j], num_linha, col)
                i = j

            elif c == "'" and i + 2 < n and linha[i + 2] == "'":
                novo("CARACTER", linha[i:i + 3], num_linha, col)
                i += 3

            elif c == '"':
                j = linha.find('"', i + 1)
                j = n if j == -1 else j + 1
                novo("TEXTO", linha[i:j], num_linha, col)
                i = j

            elif linha[i:i + 2] in OPERADORES_DUPLOS:
                novo(OPERADORES_DUPLOS[linha[i:i + 2]], linha[i:i + 2], num_linha, col)
                i += 2

            elif c in SIMBOLOS:
                novo(SIMBOLOS[c], c, num_linha, col)
                i += 1

            else:
                novo("DESCONHECIDO", c, num_linha, col)
                i += 1
    return tokens


# -------------------------------------------------------------- sintático

def verificar_delimitadores(tokens):
    """Valida o balanceamento com uma pilha e preenche token.ref.
    Retorna a lista de mensagens de erro (vazia se tudo estiver correto)."""
    pilha, erros = [], []

    for tok in tokens:
        if tok.tipo in NOME:                       # abertura: empilha
            pilha.append(tok)

        elif tok.tipo in PAR_DE:                   # fechamento: desempilha
            esperado = PAR_DE[tok.tipo]
            if not pilha:
                erros.append(f"linha {tok.linha}, coluna {tok.coluna}: '{tok.lexema}' "
                             f"fecha {NOME[esperado]} que não foi aberto")
                continue
            topo = pilha[-1]
            if topo.tipo == esperado:
                pilha.pop()
                tok.ref = topo.id
            else:
                # fechamento não corresponde ao último aberto: reporta e ignora
                erros.append(f"linha {tok.linha}, coluna {tok.coluna}: '{tok.lexema}' "
                             f"inesperado, esperado fechamento de '{topo.lexema}' "
                             f"(ID {topo.id}, linha {topo.linha})")

    for tok in pilha:
        erros.append(f"linha {tok.linha}, coluna {tok.coluna}: '{tok.lexema}' "
                     f"(ID {tok.id}) nunca foi fechado")
    return erros


def contar_delimitadores(tokens):
    """Contagem de aberturas e fechamentos de cada par, exigida no enunciado."""
    contagem = {}
    for abre, fecha in (("(", ")"), ("{", "}"), ("[", "]")):
        contagem[abre + fecha] = (sum(t.lexema == abre for t in tokens),
                                  sum(t.lexema == fecha for t in tokens))
    return contagem


# ------------------------------------------------------------------- main

def gravar_tabela(tokens, caminho):
    with open(caminho, "w", encoding="utf-8", newline="") as arq:
        escritor = csv.writer(arq, delimiter=";")
        escritor.writerow(["ID", "token", "tipo", "linha", "coluna", "Ref"])
        for t in tokens:
            escritor.writerow([t.id, t.lexema, t.tipo, t.linha, t.coluna,
                               "" if t.ref is None else t.ref])


def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PASTA, "input.c")
    with open(entrada, encoding="utf-8") as arq:
        tokens = analisar_lexico(arq.read())

    erros = verificar_delimitadores(tokens)
    contagem = contar_delimitadores(tokens)

    nome = os.path.splitext(os.path.basename(entrada))[0]
    saida = "tabela_simbolos.csv" if nome == "input" else f"tabela_simbolos_{nome}.csv"
    gravar_tabela(tokens, os.path.join(PASTA, saida))

    print(f"Arquivo: {os.path.basename(entrada)}  ({len(tokens)} tokens)\n")
    print(f"{'ID':>4}  {'token':<12} {'tipo':<14} {'lin':>3} {'col':>3}  Ref")
    for t in tokens:
        if t.tipo in NOME or t.tipo in PAR_DE:
            ref = "" if t.ref is None else t.ref
            print(f"{t.id:>4}  {t.lexema:<12} {t.tipo:<14} {t.linha:>3} {t.coluna:>3}  {ref}")

    print("\nContagem (abre / fecha):")
    for par, (abre, fecha) in contagem.items():
        situacao = "OK" if abre == fecha else "DIFERENTE"
        print(f"  {par}  {abre} / {fecha}  {situacao}")

    if erros:
        print(f"\n[ERRO] {len(erros)} problema(s) de balanceamento:")
        for e in erros:
            print("  - " + e)
    else:
        print("\n[OK] Todos os delimitadores estão balanceados e aninhados corretamente.")
    print(f"\nTabela de símbolos gravada em {saida}")


if __name__ == "__main__":
    main()
