import csv
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

# Mapeamento de tipos primitivos da gramática
TIPOS_VALIDOS = {
    "int": "PR:INT",
    "char": "PR:CHAR",
    "float": "PR:FLOAT",
    "double": "PR:DOUBLE",
    "void": "PR:VOID",
    "boolean": "PR:BOOLEAN",
}

# Literais booleanos aceitos
LITERAIS_BOOL = {
    "true": "PR:TRUE",
    "false": "PR:FALSE",
}

# Conjunto de tipos permitidos no lado direito da inicialização
VALORES_PERMITIDOS = {
    "INTEIRO",
    "FRACIONARIO",
    "NOMEVARIAVEL",
    "PR:TRUE",
    "PR:FALSE",
}

# Expressão regular para segmentação dos tokens na linha
REGEX_TOKEN = re.compile(
    r"[+-]?(?:\d+\.\d+|\.\d+)|[+-]?\d+|"
    r"[A-Za-z_][A-Za-z0-9_]*|==|<=|>=|!=|[,;=<>!]|[^\s]"
)


@dataclass
class Simbolo:
    """Estrutura para armazenar o token e sua localização no código."""
    lexema: str
    tipo: str
    linha: int
    coluna: int
    valido: bool = True


@dataclass
class ElementoVar:
    """Representa uma variável declarada e sua atribuição opcional."""
    nome: str
    valor: Optional[str] = None


@dataclass
class RespostaSintatica:
    """Resultado da validação sintática da declaração."""
    sucesso: bool
    tipo: Optional[str]
    variaveis: List[ElementoVar]
    detalhe: str


def categorizar_token(lexema: str) -> Tuple[str, bool]:
    """Identifica a classe gramatical de um determinado lexema."""
    if lexema in TIPOS_VALIDOS:
        return TIPOS_VALIDOS[lexema], True

    if lexema in LITERAIS_BOOL:
        return LITERAIS_BOOL[lexema], True

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


def obter_tokens_linha(linha: str, num_linha: int) -> List[Simbolo]:
    """Varre a linha identificando todos os tokens e posições."""
    tokens = []
    for match in REGEX_TOKEN.finditer(linha):
        lexema = match.group(0)
        tipo, valido = categorizar_token(lexema)
        tokens.append(
            Simbolo(
                lexema=lexema,
                tipo=tipo,
                linha=num_linha,
                coluna=match.start() + 1,
                valido=valido,
            )
        )
    return tokens


def analisar_sintaxe(tokens: List[Simbolo]) -> RespostaSintatica:
    """
    Valida a regra unificada de declaração:
      Declara -> [TIPO] [ITEM] [PV] | [TIPO] [ITEM] DeclaraMultiplo [PV]
      DeclaraMultiplo -> [VG] [ITEM] | [VG] [ITEM] DeclaraMultiplo
      [ITEM] -> NOMEVARIAVEL | NOMEVARIAVEL ATRIBUICAO [VALOR]
    """
    if not tokens:
        return RespostaSintatica(
            sucesso=False,
            tipo=None,
            variaveis=[],
            detalhe="Linha vazia.",
        )

    tipo_base = tokens[0].tipo
    if tipo_base not in TIPOS_VALIDOS.values():
        return RespostaSintatica(
            sucesso=False,
            tipo=None,
            variaveis=[],
            detalhe="A instrução deve iniciar com um TIPO válido.",
        )

    pos = 1
    variaveis: List[ElementoVar] = []

    while True:
        if pos >= len(tokens) or tokens[pos].tipo != "NOMEVARIAVEL":
            achado = tokens[pos].lexema if pos < len(tokens) else "fim da linha"
            return RespostaSintatica(
                sucesso=False,
                tipo=tipo_base,
                variaveis=variaveis,
                detalhe=f"Esperava NOMEVARIAVEL, mas encontrou '{achado}'.",
            )

        var_nome = tokens[pos].lexema
        pos += 1
        var_valor: Optional[str] = None

        # Inicialização opcional: = VALOR
        if pos < len(tokens) and tokens[pos].tipo == "ATRIBUICAO":
            pos += 1

            if pos >= len(tokens) or tokens[pos].tipo not in VALORES_PERMITIDOS:
                achado = tokens[pos].lexema if pos < len(tokens) else "fim da linha"
                return RespostaSintatica(
                    sucesso=False,
                    tipo=tipo_base,
                    variaveis=variaveis,
                    detalhe=f"Esperava VALOR após '=' para '{var_nome}', mas encontrou '{achado}'.",
                )

            var_valor = tokens[pos].lexema
            pos += 1

        variaveis.append(ElementoVar(nome=var_nome, valor=var_valor))

        if pos >= len(tokens):
            return RespostaSintatica(
                sucesso=False,
                tipo=tipo_base,
                variaveis=variaveis,
                detalhe="Esperava PONTO_VIRGULA ao final da linha.",
            )

        # Múltiplos declaradores separados por vírgula
        if tokens[pos].tipo == "VIRGULA":
            pos += 1
            continue

        break

    if tokens[pos].tipo != "PONTO_VIRGULA":
        return RespostaSintatica(
            sucesso=False,
            tipo=tipo_base,
            variaveis=variaveis,
            detalhe=f"Esperava PONTO_VIRGULA, mas encontrou '{tokens[pos].lexema}'.",
        )

    if pos != len(tokens) - 1:
        extra = tokens[pos + 1].lexema
        return RespostaSintatica(
            sucesso=False,
            tipo=tipo_base,
            variaveis=variaveis,
            detalhe=f"Conteúdo excedente após PONTO_VIRGULA: '{extra}'.",
        )

    total_vars = len(variaveis)
    total_inits = sum(v.valor is not None for v in variaveis)
    return RespostaSintatica(
        sucesso=True,
        tipo=tipo_base,
        variaveis=variaveis,
        detalhe=f"Declaração aceita com {total_vars} variável(is) e {total_inits} inicialização(ões).",
    )


def iniciar_tabela_csv(caminho_csv: str) -> None:
    """Inicializa o arquivo CSV com os cabeçalhos padrão."""
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arq:
        csv.writer(arq, delimiter=";", lineterminator="\n").writerow(
            ["ID", "token", "tipo", "linha", "coluna"]
        )


def registrar_simbolo_csv(caminho_csv: str, identificador: int, token: Simbolo) -> None:
    """Acrescenta um token à tabela de símbolos CSV."""
    with open(caminho_csv, "a", newline="", encoding="utf-8-sig") as arq:
        csv.writer(arq, delimiter=";", lineterminator="\n").writerow(
            [identificador, token.lexema, token.tipo, token.linha, token.coluna]
        )


def exibir_tokens(tokens: List[Simbolo]) -> None:
    for tok in tokens:
        status = "ACEITO" if tok.valido else "REJEITADO"
        print(
            f"  [{status}] {tok.lexema!r} -> {tok.tipo} "
            f"(linha {tok.linha}, coluna {tok.coluna})"
        )


def exibir_resultado(resultado: RespostaSintatica) -> None:
    status = "ACEITA" if resultado.sucesso else "REJEITADA"
    categoria = "DECLARA_MULTIPLO" if len(resultado.variaveis) > 1 else "DECLARA"

    print(f"  [DECLARACAO {status} - {categoria}]")
    if resultado.tipo is not None:
        print(f"  Tipo: {resultado.tipo}")
    if resultado.variaveis:
        itens = [
            v.nome if v.valor is None else f"{v.nome} = {v.valor}"
            for v in resultado.variaveis
        ]
        print(f"  Declaradores: {', '.join(itens)}")
    print(f"  Mensagem: {resultado.detalhe}")


def processar_fonte(caminho_entrada: str, caminho_csv: str) -> None:
    iniciar_tabela_csv(caminho_csv)
    id_atual = 1

    with open(caminho_entrada, "r", encoding="utf-8") as arq:
        for num_linha, linha in enumerate(arq, start=1):
            tokens = obter_tokens_linha(linha, num_linha)

            if not tokens:
                continue

            print(f"\nLinha {num_linha}: {linha.rstrip()}")
            exibir_tokens(tokens)

            for tok in tokens:
                if tok.valido:
                    registrar_simbolo_csv(caminho_csv, id_atual, tok)
                    id_atual += 1

            resultado = analisar_sintaxe(tokens)
            exibir_resultado(resultado)


def main() -> None:
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_input = os.path.join(diretorio, "input.c")
    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")

    if not os.path.exists(caminho_input):
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {caminho_input}")

    processar_fonte(caminho_input, caminho_csv)
    print(f"\nTabela de símbolos salva em: {caminho_csv}")


if __name__ == "__main__":
    main()
