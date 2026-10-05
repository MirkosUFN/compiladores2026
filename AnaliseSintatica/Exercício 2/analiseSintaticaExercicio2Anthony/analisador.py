import csv
import os
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

# =====================================================================
# TABELAS E MAPEAMENTOS LÉXICOS
# =====================================================================

TIPOS_VALIDOS = {
    "int": "PR:INT",
    "char": "PR:CHAR",
    "float": "PR:FLOAT",
    "double": "PR:DOUBLE",
    "void": "PR:VOID",
    "boolean": "PR:BOOLEAN",
}

LITERAIS_BOOL = {
    "true": "PR:TRUE",
    "false": "PR:FALSE",
}

DELIMITADORES_ABERTURA = {
    "(": "ABRE_PARENTESES",
    "{": "ABRE_CHAVES",
    "[": "ABRE_COLCHETES",
}

DELIMITADORES_FECHAMENTO = {
    ")": "FECHA_PARENTESES",
    "}": "FECHA_CHAVES",
    "]": "FECHA_COLCHETES",
}

MAPA_FECHA_PARA_ABRE = {
    ")": "(",
    "}": "{",
    "]": "[",
}

OPERADORES = {
    "+": "OPERADOR_SOMA",
    "-": "OPERADOR_SUBTRACAO",
    "*": "OPERADOR_MULTIPLICACAO",
    "/": "OPERADOR_DIVISAO",
    "==": "OPERADOR_IGUALDADE",
    "!=": "OPERADOR_DIFERENTE",
    "<=": "OPERADOR_MENOR_IGUAL",
    ">=": "OPERADOR_MAIOR_IGUAL",
    "<": "OPERADOR_MENOR",
    ">": "OPERADOR_MAIOR",
}

REGEX_TOKEN = re.compile(
    r"[+-]?(?:\d+\.\d+|\.\d+)|[+-]?\d+|"
    r"[A-Za-z_][A-Za-z0-9_]*|==|<=|>=|!=|"
    r"[(){}\[\]]|[,;=<>!+\-*/]|[^\s]"
)


# =====================================================================
# ESTRUTURAS DE DADOS
# =====================================================================

@dataclass
class Simbolo:
    """Representa um token com sua posição e referência na tabela de símbolos."""
    id: int
    lexema: str
    tipo: str
    linha: int
    coluna: int
    valido: bool = True
    ref: Optional[int] = None


@dataclass
class ResultadoAnalise:
    """Resultado da validação de delimitadores e contagens."""
    sucesso: bool
    contagem_abre: Dict[str, int]
    contagem_fecha: Dict[str, int]
    erros: List[str]


# =====================================================================
# ANÁLISE LÉXICA
# =====================================================================

def categorizar_token(lexema: str) -> Tuple[str, bool]:
    """Identifica a classe gramatical de um determinado lexema."""
    if lexema in TIPOS_VALIDOS:
        return TIPOS_VALIDOS[lexema], True
    if lexema in LITERAIS_BOOL:
        return LITERAIS_BOOL[lexema], True
    if lexema in DELIMITADORES_ABERTURA:
        return DELIMITADORES_ABERTURA[lexema], True
    if lexema in DELIMITADORES_FECHAMENTO:
        return DELIMITADORES_FECHAMENTO[lexema], True
    if lexema in OPERADORES:
        return OPERADORES[lexema], True
    if re.fullmatch(r"[+-]?\d+", lexema):
        return "INTEIRO", True
    if re.fullmatch(r"[+-]?(?:\d+\.\d+|\.\d+)", lexema):
        return "FRACIONARIO", True
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", lexema):
        return "NOMEVARIAVEL", True
    if lexema == "=":
        return "ATRIBUICAO", True
    if lexema == ",":
        return "VIRGULA", True
    if lexema == ";":
        return "PONTO_VIRGULA", True
    return "DESCONHECIDO", False


def extrair_tokens(caminho_entrada: str) -> List[Simbolo]:
    """Lê o arquivo fonte e extrai sequencialmente todos os tokens com seus IDs."""
    tokens: List[Simbolo] = []
    id_atual = 1

    with open(caminho_entrada, "r", encoding="utf-8") as arq:
        for num_linha, linha in enumerate(arq, start=1):
            for match in REGEX_TOKEN.finditer(linha):
                lexema = match.group(0)
                tipo, valido = categorizar_token(lexema)
                tokens.append(
                    Simbolo(
                        id=id_atual,
                        lexema=lexema,
                        tipo=tipo,
                        linha=num_linha,
                        coluna=match.start() + 1,
                        valido=valido,
                    )
                )
                id_atual += 1

    return tokens


# =====================================================================
# ANÁLISE SINTÁTICA DE DELIMITADORES (PILHA & CONTAGEM IDÊNTICA)
# =====================================================================

def analisar_delimitadores(tokens: List[Simbolo]) -> ResultadoAnalise:
    """Valida a contagem idêntica e o aninhamento dos delimitadores via pilha (LIFO)."""
    pilha: List[Simbolo] = []
    erros: List[str] = []
    cont_abre = {"(": 0, "{": 0, "[": 0}
    cont_fecha = {")": 0, "}": 0, "]": 0}

    for tok in tokens:
        if not tok.valido:
            continue

        if tok.lexema in DELIMITADORES_ABERTURA:
            cont_abre[tok.lexema] += 1
            pilha.append(tok)

        elif tok.lexema in DELIMITADORES_FECHAMENTO:
            cont_fecha[tok.lexema] += 1
            esperado = MAPA_FECHA_PARA_ABRE[tok.lexema]

            if not pilha:
                erros.append(
                    f"Fechamento '{tok.lexema}' (ID {tok.id}, L{tok.linha}, C{tok.coluna}) sem abertura correspondente."
                )
            elif pilha[-1].lexema == esperado:
                abertura = pilha.pop()
                tok.ref = abertura.id
            else:
                topo = pilha[-1]
                erros.append(
                    f"Fechamento '{tok.lexema}' (ID {tok.id}, L{tok.linha}, C{tok.coluna}) "
                    f"incompatível com abertura '{topo.lexema}' (ID {topo.id}, L{topo.linha}, C{topo.coluna})."
                )

    while pilha:
        orfao = pilha.pop()
        erros.append(
            f"Abertura '{orfao.lexema}' (ID {orfao.id}, L{orfao.linha}, C{orfao.coluna}) não foi fechada."
        )

    for abre, fecha in [("(", ")"), ("{", "}"), ("[", "]")]:
        if cont_abre[abre] != cont_fecha[fecha]:
            erros.append(
                f"Contagem divergente para '{abre} {fecha}': {cont_abre[abre]} abre vs {cont_fecha[fecha]} fecha."
            )

    return ResultadoAnalise(
        sucesso=(len(erros) == 0),
        contagem_abre=cont_abre,
        contagem_fecha=cont_fecha,
        erros=erros,
    )


# =====================================================================
# PERSISTÊNCIA E EXIBIÇÃO
# =====================================================================

def salvar_tabela_simbolos_csv(caminho_csv: str, tokens: List[Simbolo]) -> None:
    """Grava a tabela de símbolos no formato CSV com a coluna 'Ref'."""
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arq:
        escritor = csv.writer(arq, delimiter=";", lineterminator="\n")
        escritor.writerow(["ID", "token", "tipo", "linha", "coluna", "Ref"])
        for tok in tokens:
            ref_str = str(tok.ref) if tok.ref is not None else ""
            escritor.writerow([tok.id, tok.lexema, tok.tipo, tok.linha, tok.coluna, ref_str])


def exibir_relatorio(tokens: List[Simbolo], resultado: ResultadoAnalise, caminho_csv: str) -> None:
    """Exibe o relatório de contagem, referências e resultado final."""
    print("=" * 65)
    print(" ANALISADOR SINTÁTICO - DELIMITADORES ((), {}, [])")
    print("=" * 65)

    print("\n--- 1. CONTAGEM COMPARATIVA DE DELIMITADORES ---")
    print(f"{'Delimitador':<16} | {'Abre':<6} | {'Fecha':<6} | {'Status'}")
    print("-" * 50)
    pares = [("Parênteses ( )", "(", ")"), ("Chaves { }", "{", "}"), ("Colchetes [ ]", "[", "]")]
    for nome, a, f in pares:
        qa, qf = resultado.contagem_abre[a], resultado.contagem_fecha[f]
        status = "[OK - IDÊNTICO]" if qa == qf else f"[ERRO - DIFF {qa - qf:+d}]"
        print(f"{nome:<16} | {qa:<6} | {qf:<6} | {status}")

    fechamentos = [t for t in tokens if t.ref is not None]
    print(f"\n--- 2. PAREAMENTO NA PILHA (Coluna Ref - {len(fechamentos)} pares) ---")
    for f in fechamentos:
        print(f"  Token {f.id:02d} '{f.lexema}' (L{f.linha}, C{f.coluna}) -> Ref ID {f.ref:02d}")

    print("\n" + "=" * 65)
    if resultado.sucesso:
        print("[STATUS: ACEITO] Todos os delimitadores possuem contagem idêntica e aninhamento correto.")
    else:
        print("[STATUS: REJEITADO]")
        for erro in resultado.erros:
            print(f"  [!] {erro}")

    print(f"\nTabela de símbolos salva em:\n{caminho_csv}")
    print("=" * 65)


def main() -> None:
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_input = os.path.join(diretorio, "input.c")
    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")

    if not os.path.exists(caminho_input):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho_input}")

    tokens = extrair_tokens(caminho_input)
    resultado = analisar_delimitadores(tokens)
    salvar_tabela_simbolos_csv(caminho_csv, tokens)
    exibir_relatorio(tokens, resultado, caminho_csv)


if __name__ == "__main__":
    main()
