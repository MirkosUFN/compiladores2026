"""
Analisador Sintático, Léxico e Balanceador de Delimitadores
"""

import csv
import os
import re
import sys
from dataclasses import dataclass
from typing import List, Optional, Tuple

# Suporte a UTF-8 no terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


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

TIPOS_DE_VALOR = {
    "INTEIRO",
    "FRACIONARIO",
    "NOMEVARIAVEL",
    "PR:TRUE",
    "PR:FALSE",
    "LITERAL_CARACTERE",
    "LITERAL_TEXTO",
}

PADRAO_TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"'
    r"|'(?:\\.|[^'\\])*'"
    r"|[+-]?(?:\d+\.\d+|\.\d+)|[+-]?\d+"
    r"|[A-Za-z_][A-Za-z0-9_]*"
    r"|==|<=|>=|!="
    r"|[()\[\]{},;=+\-*/<>!]"
    r"|[^\s]"
)


@dataclass
class Token:
    """Token reconhecido, com a posição e referências para a Tabela de Símbolos."""

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


class NodoSintatico:
    """Nó para representação hierárquica da Árvore de Derivação Sintática."""

    def __init__(self, nome: str, valor: Optional[str] = None):
        self.nome = nome
        self.valor = valor
        self.filhos: List["NodoSintatico"] = []

    def adicionar_filho(self, filho: "NodoSintatico") -> "NodoSintatico":
        self.filhos.append(filho)
        return filho

    def formatar(self, prefixo: str = "", eh_ultimo: bool = True) -> List[str]:
        linhas = []
        conector = "└── " if eh_ultimo else "├── "
        rotulo = f"{self.nome}: {self.valor}" if self.valor is not None else self.nome
        linhas.append(f"{prefixo}{conector}{rotulo}")

        prefixo_filho = prefixo + ("    " if eh_ultimo else "│   ")
        for i, filho in enumerate(self.filhos):
            ultimo = i == len(self.filhos) - 1
            linhas.extend(filho.formatar(prefixo_filho, ultimo))
        return linhas


@dataclass
class ResultadoSintatico:
    """Resultado do reconhecimento de um comando ou estrutura sintática."""

    aceito: bool
    regra: str
    mensagem: str
    arvore: Optional[NodoSintatico] = None


def classificar_lexema(lexema: str) -> Tuple[str, bool]:
    """Classifica um lexema nos terminais utilizados pela gramática."""
    if lexema in TIPOS:
        return TIPOS[lexema], True

    if lexema in VALORES_BOOLEANOS:
        return VALORES_BOOLEANOS[lexema], True

    if lexema == "if":
        return "PR:IF", True

    if lexema == "else":
        return "PR:ELSE", True

    if lexema in DELIMITADORES_ABERTURA:
        return DELIMITADORES_ABERTURA[lexema], True

    if lexema in DELIMITADORES_FECHAMENTO:
        return DELIMITADORES_FECHAMENTO[lexema], True

    if lexema.startswith("'") and lexema.endswith("'") and len(lexema) >= 2:
        return "LITERAL_CARACTERE", True

    if lexema.startswith('"') and lexema.endswith('"') and len(lexema) >= 2:
        return "LITERAL_TEXTO", True

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

    if lexema in {"<", ">", "==", "<=", ">=", "!="}:
        return "SINAL_COMPARACAO", True

    if lexema in {"+", "-", "*", "/"}:
        return "OPERADOR_ARITMETICO", True

    return "NAO_RECONHECIDO", False


def tokenizar_linha(linha: str, numero_linha: int) -> List[Token]:
    """Tokeniza uma linha registrando lexemas e coordenadas."""
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


def atribuir_identificadores(linhas_tokens: List[List[Token]]) -> int:
    """Atribui IDs numéricos sequenciais para os tokens aceitos."""
    proximo_id = 1
    for linha in linhas_tokens:
        for token in linha:
            if token.aceito:
                token.identificador = proximo_id
                proximo_id += 1
    return proximo_id


def analisar_delimitadores(tokens: List[Token]) -> ResultadoDelimitadores:
    """
    Valida a quantidade, ordem e aninhamento dos delimitadores ( ) { } [ ].
    Preenche a propriedade 'ref' nos tokens de fechamento apontando para a abertura.
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
                    f"'{abertura.lexema}' (ID {abertura.identificador}) "
                    f"na linha {token.linha}, coluna {token.coluna}."
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
                f"Abertura '{abertura.lexema}' (ID {abertura.identificador}) "
                f"na linha {abertura.linha}, coluna {abertura.coluna} "
                "não possui fechamento correspondente."
            ),
            pares=pares,
        )

    return ResultadoDelimitadores(
        aceito=True,
        mensagem=f"Delimitadores balanceados com sucesso! {pares} par(es) validado(s).",
        pares=pares,
    )


# --- ANALISADOR SINTÁTICO ADAPTADO PARA A GRAMÁTICA SINTAXE.TXT ---


def analisar_comando(tokens: List[Token]) -> ResultadoSintatico:
    """
    Analisador Sintático modularizado conforme as regras de sintaxe.txt:
    - Declaração (Declara)
    - Condicional (if/else)
    - Atribuição (Atribuicao)
    - Bloco ({ })
    """
    if not tokens:
        return ResultadoSintatico(aceito=False, regra="-", mensagem="Linha vazia.")

    primeiro = tokens[0]

    # 1. Regra: Declara -> TIPO DECLARADOR ... PV
    if primeiro.tipo in set(TIPOS.values()):
        return _analisar_declaracao(tokens)

    # 2. Regra: Condicional -> PR:IF AP ExpressaoRelacional FP ...
    if primeiro.tipo == "PR:IF":
        return _analisar_condicional(tokens)

    # 3. Regra: Bloco -> AC ... FC
    if primeiro.tipo == "ABRE_CHAVE":
        return ResultadoSintatico(
            aceito=True,
            regra="Bloco",
            mensagem="Abertura de bloco identificada.",
            arvore=NodoSintatico("Bloco", "{"),
        )
    if primeiro.tipo == "FECHA_CHAVE":
        return ResultadoSintatico(
            aceito=True,
            regra="Bloco",
            mensagem="Fechamento de bloco identificado.",
            arvore=NodoSintatico("Bloco", "}"),
        )

    # 4. Regra: Atribuicao -> NOMEVARIAVEL ATRIBUICAO VALOR PV
    if primeiro.tipo == "NOMEVARIAVEL":
        return _analisar_atribuicao(tokens)

    return ResultadoSintatico(
        aceito=False,
        regra="-",
        mensagem=f"Sintaxe não reconhecida começando por '{primeiro.lexema}'.",
    )


def _analisar_declaracao(tokens: List[Token]) -> ResultadoSintatico:
    tipo = tokens[0].tipo
    declaradores = []
    i = 1

    while i < len(tokens):
        if tokens[i].tipo != "NOMEVARIAVEL":
            return ResultadoSintatico(
                aceito=False,
                regra="Declara",
                mensagem=f"Esperado NOMEVARIAVEL, mas encontrado '{tokens[i].lexema}'.",
            )
        nome = tokens[i].lexema
        valor = None
        i += 1

        if i < len(tokens) and tokens[i].tipo == "ATRIBUICAO":
            i += 1
            if i >= len(tokens) or tokens[i].tipo not in TIPOS_DE_VALOR:
                return ResultadoSintatico(
                    aceito=False,
                    regra="Declara",
                    mensagem=f"Valor inválido na inicialização de '{nome}'.",
                )
            valor = tokens[i].lexema
            i += 1

        declaradores.append((nome, valor))

        if i < len(tokens) and tokens[i].tipo == "VIRGULA":
            i += 1
            continue
        break

    if i >= len(tokens) or tokens[i].tipo != "PONTO_VIRGULA":
        return ResultadoSintatico(
            aceito=False,
            regra="Declara",
            mensagem="Esperado PONTO_VIRGULA ao final da declaração.",
        )

    regra_nome = "DeclaraMultiplo" if len(declaradores) > 1 else "Declara"
    
    # Monta Árvore Sintática
    raiz = NodoSintatico(regra_nome)
    raiz.adicionar_filho(NodoSintatico("[TIPO]", tipo))
    for nom, val in declaradores:
        d_node = NodoSintatico("DECLARADOR")
        d_node.adicionar_filho(NodoSintatico("[NOMEVARIAVEL]", nom))
        if val:
            inic = NodoSintatico("INICIALIZACAO")
            inic.adicionar_filho(NodoSintatico("[ATRIBUICAO]", "="))
            inic.adicionar_filho(NodoSintatico("[VALOR]", val))
            d_node.adicionar_filho(inic)
        raiz.adicionar_filho(d_node)
    raiz.adicionar_filho(NodoSintatico("[PV]", ";"))

    return ResultadoSintatico(
        aceito=True,
        regra=regra_nome,
        mensagem=f"Declaração válida ({len(declaradores)} variável(is)).",
        arvore=raiz,
    )


def _analisar_condicional(tokens: List[Token]) -> ResultadoSintatico:
    # Condicional -> PR:IF AP ExpressaoRelacional FP ...
    if len(tokens) < 5:
        return ResultadoSintatico(
            aceito=False,
            regra="Condicional",
            mensagem="Comando IF incompleto.",
        )

    if tokens[1].tipo != "ABRE_PARENTESE":
        return ResultadoSintatico(
            aceito=False,
            regra="Condicional",
            mensagem="Esperado '(' após 'if'.",
        )

    # ExpressaoRelacional: VALOR SINAL_COMPARACAO VALOR
    if (
        tokens[2].tipo not in TIPOS_DE_VALOR
        or tokens[3].tipo != "SINAL_COMPARACAO"
        or tokens[4].tipo not in TIPOS_DE_VALOR
    ):
        return ResultadoSintatico(
            aceito=False,
            regra="Condicional",
            mensagem="Expressão relacional inválida dentro do 'if'. Exemplo esperado: 'a > b'.",
        )

    if len(tokens) <= 5 or tokens[5].tipo != "FECHA_PARENTESE":
        return ResultadoSintatico(
            aceito=False,
            regra="Condicional",
            mensagem="Esperado ')' após a expressão relacional.",
        )

    raiz = NodoSintatico("Condicional")
    raiz.adicionar_filho(NodoSintatico("PR:IF", "if"))
    raiz.adicionar_filho(NodoSintatico("[AP]", "("))
    
    exp = NodoSintatico("ExpressaoRelacional")
    exp.adicionar_filho(NodoSintatico("[VALOR]", tokens[2].lexema))
    exp.adicionar_filho(NodoSintatico("[SINAL_COMPARACAO]", tokens[3].lexema))
    exp.adicionar_filho(NodoSintatico("[VALOR]", tokens[4].lexema))
    raiz.adicionar_filho(exp)
    raiz.adicionar_filho(NodoSintatico("[FP]", ")"))

    return ResultadoSintatico(
        aceito=True,
        regra="Condicional",
        mensagem="Estrutura condicional (IF) reconhecida.",
        arvore=raiz,
    )


def _analisar_atribuicao(tokens: List[Token]) -> ResultadoSintatico:
    # Atribuicao -> NOMEVARIAVEL ATRIBUICAO VALOR PV
    if (
        len(tokens) >= 4
        and tokens[1].tipo == "ATRIBUICAO"
        and tokens[2].tipo in TIPOS_DE_VALOR
        and tokens[3].tipo == "PONTO_VIRGULA"
    ):
        raiz = NodoSintatico("Atribuicao")
        raiz.adicionar_filho(NodoSintatico("[NOMEVARIAVEL]", tokens[0].lexema))
        raiz.adicionar_filho(NodoSintatico("[ATRIBUICAO]", "="))
        raiz.adicionar_filho(NodoSintatico("[VALOR]", tokens[2].lexema))
        raiz.adicionar_filho(NodoSintatico("[PV]", ";"))

        return ResultadoSintatico(
            aceito=True,
            regra="Atribuicao",
            mensagem="Atribuição reconhecida com sucesso.",
            arvore=raiz,
        )

    return ResultadoSintatico(
        aceito=False,
        regra="Atribuicao",
        mensagem="Sintaxe de atribuição inválida. Esperado: var = valor;",
    )


# --- FUNÇÕES AUXILIARES E IO ---


def carregar_sintaxe(caminho_sintaxe: str) -> List[str]:
    regras: List[str] = []
    if not os.path.exists(caminho_sintaxe):
        return regras
    with open(caminho_sintaxe, "r", encoding="utf-8") as arq:
        for linha in arq:
            linha_limpa = linha.strip()
            if linha_limpa and not linha_limpa.startswith("#"):
                regras.append(linha_limpa)
    return regras


def exibir_sintaxe(regras: List[str], caminho_sintaxe: str) -> None:
    nome = os.path.basename(caminho_sintaxe)
    print(f"[*] Gramática carregada de: {nome}")
    for regra in regras:
        print(f"    {regra}")
    print("=" * 65)


def criar_tabela_simbolos(caminho_csv: str) -> None:
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow(
            ["ID", "token", "tipo", "linha", "coluna", "Ref"]
        )


def adicionar_simbolo(caminho_csv: str, token: Token) -> None:
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


def imprimir_tabela(dados: List[dict], colunas: List[str], titulo: Optional[str] = None) -> None:
    if not dados:
        print("\n[!] Tabela vazia.")
        return

    if titulo:
        print(f"\n=== {titulo} ===")

    larguras = {col: len(col) for col in colunas}
    for item in dados:
        for col in colunas:
            val = str(item.get(col, ""))
            if len(val) > larguras[col]:
                larguras[col] = len(val)

    separador = "+" + "+".join("-" * (larguras[col] + 2) for col in colunas) + "+"
    cabecalho = "|" + "|".join(f" {col:<{larguras[col]}} " for col in colunas) + "|"

    print(separador)
    print(cabecalho)
    print(separador)
    for item in dados:
        linha_str = "|" + "|".join(f" {str(item.get(col, '')):<{larguras[col]}} " for col in colunas) + "|"
        print(linha_str)
    print(separador)


def mostrar_tokens(tokens: List[Token]) -> None:
    for token in tokens:
        status = "ACEITO" if token.aceito else "REJEITADO"
        ref_str = f" | Ref -> {token.ref}" if token.ref is not None else ""
        id_str = f"ID #{token.identificador} | " if token.identificador else ""
        print(
            f"  [{status}] {id_str}{token.lexema!r} -> {token.tipo} "
            f"(linha {token.linha}, coluna {token.coluna}){ref_str}"
        )


def mostrar_declaracao(resultado: ResultadoSintatico) -> None:
    status = "ACEITA" if resultado.aceito else "REJEITADA"
    print(f"  [ANÁLISE SINTÁTICA {status} | Regra: {resultado.regra}]")
    print(f"  Mensagem: {resultado.mensagem}")

    if resultado.arvore is not None:
        print("  Árvore de Derivação:")
        for linha in resultado.arvore.formatar(prefixo="    "):
            print(linha)


def processar_arquivo(caminho_entrada: str, caminho_csv: str) -> None:
    linhas_tokens: List[List[Token]] = []

    # 1. Tokenização
    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            tokens = tokenizar_linha(linha, numero_linha)
            linhas_tokens.append(tokens)

    # 2. Atribuição de IDs
    atribuir_identificadores(linhas_tokens)

    # 3. Análise Global de Delimitadores (Alimenta o campo 'ref')
    todos_tokens = [t for linha in linhas_tokens for t in linha]
    resultado_delimitadores = analisar_delimitadores(todos_tokens)

    # 4. Geração da Tabela de Símbolos CSV
    criar_tabela_simbolos(caminho_csv)
    tabela_simbolos_memoria = []

    for token in todos_tokens:
        if token.aceito:
            adicionar_simbolo(caminho_csv, token)
            tabela_simbolos_memoria.append(
                {
                    "ID": token.identificador,
                    "token": token.lexema,
                    "tipo": token.tipo,
                    "linha": token.linha,
                    "coluna": token.coluna,
                    "Ref": token.ref if token.ref is not None else "",
                }
            )

    # 5. Análise Sintática Por Linha
    relatorio_sintatico = []

    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        linhas_texto = arquivo.readlines()

    for idx, tokens in enumerate(linhas_tokens, start=1):
        linha_texto = linhas_texto[idx - 1].strip() if idx <= len(linhas_texto) else ""
        if not linha_texto or not tokens:
            continue

        print(f"\n{'-' * 65}")
        print(f"Linha {idx}: {linha_texto}")
        print(f"{'-' * 65}")
        mostrar_tokens(tokens)

        # Executa o analisador sintático completo para a linha
        resultado = analisar_comando(tokens)
        mostrar_declaracao(resultado)

        status = "ACEITA" if resultado.aceito else "REJEITADA"
        relatorio_sintatico.append(
            {
                "Linha": idx,
                "Código": linha_texto,
                "Regra": resultado.regra,
                "Status": status,
                "Mensagem": resultado.mensagem,
            }
        )

    # Exibição do Balanceamento de Delimitadores
    status_del = "ACEITA" if resultado_delimitadores.aceito else "REJEITADA"
    print(f"\n[ANÁLISE DE DELIMITADORES {status_del}]")
    print(f"  {resultado_delimitadores.mensagem}")

    # Exibição das Tabelas Formatadas
    imprimir_tabela(
        tabela_simbolos_memoria,
        ["ID", "token", "tipo", "linha", "coluna", "Ref"],
        "TABELA DE SÍMBOLOS",
    )

    imprimir_tabela(
        relatorio_sintatico,
        ["Linha", "Código", "Regra", "Status", "Mensagem"],
        "RESUMO DA ANÁLISE SINTÁTICA",
    )


def main() -> None:
    diretorio = os.path.dirname(os.path.abspath(__file__))

    if len(sys.argv) > 1:
        caminho_entrada = sys.argv[1]
    else:
        caminho_entrada = os.path.join(diretorio, "input.c")

    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")
    caminho_sintaxe = os.path.join(diretorio, "sintaxe.txt")

    if not os.path.exists(caminho_entrada):
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {caminho_entrada}")

    nome_arquivo = os.path.basename(caminho_entrada)
    print("=" * 65)
    print(" ANALISADOR SINTÁTICO COMPLETO E BALANCEADOR DE DELIMITADORES ")
    print(f" Arquivo analisado: {nome_arquivo}")
    print("=" * 65)

    regras = carregar_sintaxe(caminho_sintaxe)
    exibir_sintaxe(regras, caminho_sintaxe)

    processar_arquivo(caminho_entrada, caminho_csv)
    print(f"\n[+] Tabela de símbolos salva em: {caminho_csv}")
    print("=" * 65)


if __name__ == "__main__":
    main()