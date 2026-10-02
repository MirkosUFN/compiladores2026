import csv
import os
import re
from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple


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

PADRAO_TOKEN = re.compile(
    r"[+-]?(?:\d+\.\d+|\.\d+)|[+-]?\d+|"
    r"[A-Za-z_][A-Za-z0-9_]*|==|<=|>=|!=|[,;=<>!]|[^\s]"
)


@dataclass
class Token:
    """Token reconhecido, com a posição original na linha."""

    lexema: str
    tipo: str
    linha: int
    coluna: int
    aceito: bool = True


@dataclass
class Declarador:
    """Nome de variável e seu valor inicial opcional (já formatado para exibição)."""

    nome: str
    valor: Optional[str] = None


@dataclass
class ResultadoSintatico:
    """Resultado do reconhecimento de uma linha de declaração."""

    aceito: bool
    tipo: Optional[str]
    regra: str
    declaradores: List[Declarador] = field(default_factory=list)
    mensagem: str = ""


def classificar_lexema(lexema: str) -> Tuple[str, bool]:
    """Classifica um lexema nos terminais utilizados pela gramática (sintaxe.txt)."""
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

    if lexema == "=":
        return "SATR", True

    if lexema == ",":
        return "VG", True

    if lexema == ";":
        return "PV", True

    if lexema == "'":
        return "ASPAS", True

    return "NAO_RECONHECIDO", False


def tokenizar_linha(linha: str, numero_linha: int) -> List[Token]:
    """Tokeniza uma linha e reclassifica caractere entre aspas simples como CARACTER."""
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

    # ASPAS X ASPAS, com X de um único caractere, forma o terminal CARACTER
    # (a regra DecIniChar exige [ASPAS][CARACTER][ASPAS]).
    for indice in range(len(tokens) - 2):
        anterior, meio, proximo = tokens[indice], tokens[indice + 1], tokens[indice + 2]
        if anterior.tipo == "ASPAS" and proximo.tipo == "ASPAS" and len(meio.lexema) == 1:
            meio.tipo = "CARACTER"
            meio.aceito = True

    return tokens


def _consumir_valor_simples(
    tokens: List[Token], indice: int, tipos_aceitos: Tuple[str, ...]
) -> Tuple[Optional[str], int]:
    if indice < len(tokens) and tokens[indice].tipo in tipos_aceitos:
        return tokens[indice].lexema, indice + 1
    return None, indice


def _consumir_valor_char(tokens: List[Token], indice: int) -> Tuple[Optional[str], int]:
    if (
        indice + 2 < len(tokens)
        and tokens[indice].tipo == "ASPAS"
        and tokens[indice + 1].tipo == "CARACTER"
        and tokens[indice + 2].tipo == "ASPAS"
    ):
        return f"'{tokens[indice + 1].lexema}'", indice + 3
    return None, indice


def _consumir_valor_bool(tokens: List[Token], indice: int) -> Tuple[Optional[str], int]:
    if indice < len(tokens) and tokens[indice].tipo in ("PR:TRUE", "PR:FALSE"):
        return tokens[indice].lexema, indice + 1
    return None, indice


def _analisar_declara(tokens: List[Token], tipo: str) -> ResultadoSintatico:
    """
    Reconhece a gramática original, sem inicialização:

        Declara -> [TIPO][NOMEVARIAVEL][PV]
                 | [TIPO][NOMEVARIAVEL] DeclaraMultiplo [PV]
        DeclaraMultiplo -> [VG][NOMEVARIAVEL]
                          | [VG][NOMEVARIAVEL] DeclaraMultiplo
    """
    indice = 1
    declaradores: List[Declarador] = []

    while True:
        if indice >= len(tokens) or tokens[indice].tipo != "NOMEVARIAVEL":
            encontrado = tokens[indice].lexema if indice < len(tokens) else "fim da linha"
            return ResultadoSintatico(
                False, tipo, "DECLARA", declaradores,
                f"Era esperado NOMEVARIAVEL, mas foi encontrado '{encontrado}'.",
            )

        nome = tokens[indice].lexema
        indice += 1
        declaradores.append(Declarador(nome=nome))

        if indice >= len(tokens):
            return ResultadoSintatico(
                False, tipo, "DECLARA", declaradores,
                "Era esperado PV ao final da declaração.",
            )

        if tokens[indice].tipo == "SATR":
            return ResultadoSintatico(
                False, tipo, "DECLARA", declaradores,
                f"'{nome}' não pode ser inicializado aqui: nesta linha nenhuma variável "
                "usa '=' (regra Declara), use DecIniInt/DecIniFrac/DecIniChar/DecIniBool "
                "se quiser inicializar.",
            )

        if tokens[indice].tipo == "VG":
            indice += 1
            continue

        break

    if tokens[indice].tipo != "PV":
        return ResultadoSintatico(
            False, tipo, "DECLARA", declaradores,
            f"Era esperado PV, mas foi encontrado '{tokens[indice].lexema}'.",
        )

    if indice != len(tokens) - 1:
        return ResultadoSintatico(
            False, tipo, "DECLARA", declaradores,
            f"Token inesperado depois de PV: '{tokens[indice + 1].lexema}'.",
        )

    categoria = "DECLARA" if len(declaradores) <= 1 else "DECLARA_MULTIPLO"
    return ResultadoSintatico(
        True, tipo, categoria, declaradores,
        f"Declaração aceita ({categoria}) com {len(declaradores)} variável(is), sem inicialização.",
    )


def _analisar_declara_ini(
    tokens: List[Token],
    tipo: str,
    regra_base: str,
    consumir_valor: Callable[[List[Token], int], Tuple[Optional[str], int]],
    descricao_valor: str,
) -> ResultadoSintatico:
    """
    Reconhece as regras DecIniInt/DecIniFrac/DecIniChar/DecIniBool e seus
    respectivos REPINI*, todas no formato:

        DecIni* -> TIPO [NOMEVARIAVEL][SATR]<valor>[PV]
                 | TIPO [NOMEVARIAVEL][SATR]<valor>[REPINI*][PV]
        REPINI* -> [VG][NOMEVARIAVEL][SATR]<valor>
                 | [VG][NOMEVARIAVEL][SATR]<valor>[REPINI*]
    """
    indice = 1
    declaradores: List[Declarador] = []

    while True:
        if indice >= len(tokens) or tokens[indice].tipo != "NOMEVARIAVEL":
            encontrado = tokens[indice].lexema if indice < len(tokens) else "fim da linha"
            return ResultadoSintatico(
                False, tipo, regra_base, declaradores,
                f"Era esperado NOMEVARIAVEL, mas foi encontrado '{encontrado}'.",
            )

        nome = tokens[indice].lexema
        indice += 1

        if indice >= len(tokens) or tokens[indice].tipo != "SATR":
            encontrado = tokens[indice].lexema if indice < len(tokens) else "fim da linha"
            return ResultadoSintatico(
                False, tipo, regra_base, declaradores,
                f"Era esperado SATR ('=') depois de '{nome}', mas foi encontrado '{encontrado}'.",
            )

        indice += 1
        valor, novo_indice = consumir_valor(tokens, indice)

        if valor is None:
            encontrado = tokens[indice].lexema if indice < len(tokens) else "fim da linha"
            return ResultadoSintatico(
                False, tipo, regra_base, declaradores,
                f"Era esperado {descricao_valor} para '{nome}', mas foi encontrado '{encontrado}'.",
            )

        indice = novo_indice
        declaradores.append(Declarador(nome=nome, valor=valor))

        if indice >= len(tokens):
            return ResultadoSintatico(
                False, tipo, regra_base, declaradores,
                "Era esperado PV ao final da declaração.",
            )

        if tokens[indice].tipo == "VG":
            indice += 1
            continue

        break

    if tokens[indice].tipo != "PV":
        return ResultadoSintatico(
            False, tipo, regra_base, declaradores,
            f"Era esperado PV, mas foi encontrado '{tokens[indice].lexema}'.",
        )

    if indice != len(tokens) - 1:
        return ResultadoSintatico(
            False, tipo, regra_base, declaradores,
            f"Token inesperado depois de PV: '{tokens[indice + 1].lexema}'.",
        )

    categoria = regra_base if len(declaradores) <= 1 else f"{regra_base}_MULTIPLO"
    return ResultadoSintatico(
        True, tipo, categoria, declaradores,
        f"Declaração aceita ({categoria}) com {len(declaradores)} variável(is) inicializada(s).",
    )


def analisar_declaracao(tokens: List[Token]) -> ResultadoSintatico:
    """Ponto de entrada: decide entre Declara (sem init) e DeclaraIni (com init)."""
    if not tokens:
        return ResultadoSintatico(False, None, "VAZIA", [], "Linha vazia.")

    tipo = tokens[0].tipo
    if tipo not in TIPOS.values():
        return ResultadoSintatico(
            False, None, "DESCONHECIDA", [],
            "A linha não começa com um TIPO válido.",
        )

    if len(tokens) < 2 or tokens[1].tipo != "NOMEVARIAVEL":
        encontrado = tokens[1].lexema if len(tokens) > 1 else "fim da linha"
        return ResultadoSintatico(
            False, tipo, "DESCONHECIDA", [],
            f"Era esperado NOMEVARIAVEL depois do TIPO, mas foi encontrado '{encontrado}'.",
        )

    tem_inicializacao = len(tokens) > 2 and tokens[2].tipo == "SATR"

    if tipo == "PR:VOID":
        if tem_inicializacao:
            return ResultadoSintatico(
                False, tipo, "DESCONHECIDA", [],
                "PR:VOID não possui forma de inicialização (não existe DecIniVoid).",
            )
        return _analisar_declara(tokens, tipo)

    if not tem_inicializacao:
        return _analisar_declara(tokens, tipo)

    if tipo == "PR:INT":
        return _analisar_declara_ini(
            tokens, tipo, "DECINIINT",
            lambda t, i: _consumir_valor_simples(t, i, ("INTEIRO",)),
            "INTEIRO",
        )

    if tipo in ("PR:FLOAT", "PR:DOUBLE"):
        return _analisar_declara_ini(
            tokens, tipo, "DECINIFRAC",
            lambda t, i: _consumir_valor_simples(t, i, ("FRACIONARIO",)),
            "FRACIONARIO",
        )

    if tipo == "PR:CHAR":
        return _analisar_declara_ini(
            tokens, tipo, "DECINICHAR", _consumir_valor_char, "ASPAS CARACTER ASPAS",
        )

    if tipo == "PR:BOOLEAN":
        return _analisar_declara_ini(
            tokens, tipo, "DECINIBOOL", _consumir_valor_bool, "PR:TRUE ou PR:FALSE",
        )

    return ResultadoSintatico(False, tipo, "DESCONHECIDA", [], "TIPO não tratado.")


def criar_tabela_simbolos(caminho_csv: str) -> None:
    """Cria o arquivo CSV de saída da análise léxica usada pelo exercício."""
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow(
            ["ID", "token", "tipo", "linha", "coluna"]
        )


def adicionar_simbolo(caminho_csv: str, identificador: int, token: Token) -> None:
    with open(caminho_csv, "a", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow(
            [identificador, token.lexema, token.tipo, token.linha, token.coluna]
        )


def mostrar_tokens(tokens: List[Token]) -> None:
    for token in tokens:
        status = "ACEITO" if token.aceito else "REJEITADO"
        print(
            f"  [{status}] {token.lexema!r} -> {token.tipo} "
            f"(linha {token.linha}, coluna {token.coluna})"
        )


def mostrar_declaracao(resultado: ResultadoSintatico) -> None:
    status = "ACEITA" if resultado.aceito else "REJEITADA"

    print(f"  [DECLARACAO {status} - {resultado.regra}]")
    if resultado.tipo is not None:
        print(f"  Tipo: {resultado.tipo}")
    if resultado.declaradores:
        itens = [
            item.nome if item.valor is None else f"{item.nome} = {item.valor}"
            for item in resultado.declaradores
        ]
        print(f"  Declaradores: {', '.join(itens)}")
    print(f"  Mensagem: {resultado.mensagem}")


def processar_arquivo(caminho_entrada: str, caminho_csv: str) -> None:
    criar_tabela_simbolos(caminho_csv)
    proximo_id = 1

    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            tokens = tokenizar_linha(linha, numero_linha)

            if not tokens:
                continue

            print(f"\nLinha {numero_linha}: {linha.rstrip()}")
            mostrar_tokens(tokens)

            for token in tokens:
                if token.aceito:
                    adicionar_simbolo(caminho_csv, proximo_id, token)
                    proximo_id += 1

            resultado = analisar_declaracao(tokens)
            mostrar_declaracao(resultado)


def main() -> None:
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_entrada = os.path.join(diretorio, "input.c")
    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")

    if not os.path.exists(caminho_entrada):
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {caminho_entrada}")

    processar_arquivo(caminho_entrada, caminho_csv)
    print(f"\nTabela de símbolos salva em: {caminho_csv}")


if __name__ == "__main__":
    main()
