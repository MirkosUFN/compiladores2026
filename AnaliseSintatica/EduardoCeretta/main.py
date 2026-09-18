import csv
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple


# Mapeamento de Tipos primitivos para os terminais da gramática
TIPOS = {
    "int": "PR:INT",
    "char": "PR:CHAR",
    "float": "PR:FLOAT",
    "double": "PR:DOUBLE",
    "void": "PR:VOID",
    "boolean": "PR:BOOLEAN",
}

# Literais booleanos
VALORES_BOOLEANOS = {
    "true": "BOOLEANO",
    "false": "BOOLEANO",
}

# Categorias aceitas para a regra [VALOR]
TIPOS_DE_VALOR = {
    "NUMERO",
    "CARACTERE",
    "TEXTO",
    "BOOLEANO",
    "NOMEVARIAVEL",
}

# Expressão regular para tokenizar identificadores, literais, operadores e pontuações
PADRAO_TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"'           # Literais de texto (strings entre aspas duplas)
    r"|'(?:\\.|[^'\\])'"           # Literais de caractere (entre aspas simples)
    r"|[+-]?(?:\d+\.\d+|\.\d+)"    # Literais de ponto flutuante
    r"|[+-]?\d+"                   # Literais inteiros
    r"|[A-Za-z_][A-Za-z0-9_]*"     # Identificadores e palavras-chave
    r"|==|<=|>=|!="                # Operadores relacionais compostos
    r"|[,;=<>!]"                   # Operadores simples e delimitadores
    r"|[^\s]"                      # Qualquer outro caractere não-espaço (erros/símbolos)
)


@dataclass
class Token:
    """Representa um token reconhecido com suas coordenadas no código fonte."""
    lexema: str
    tipo: str
    linha: int
    coluna: int
    aceito: bool = True


@dataclass
class Declarador:
    """Estrutura para armazenar o identificador e seu valor inicial (caso exista)."""
    nome: str
    valor: Optional[str] = None


@dataclass
class ResultadoSintatico:
    """Resultado da validação sintática da regra Declara."""
    aceito: bool
    tipo: Optional[str]
    declaradores: List[Declarador]
    mensagem: str


def classificar_lexema(lexema: str) -> Tuple[str, bool]:
    """Classifica o lexema nos tokens terminais reconhecidos pela gramática."""
    if lexema in TIPOS:
        return TIPOS[lexema], True

    if lexema in VALORES_BOOLEANOS:
        return VALORES_BOOLEANOS[lexema], True

    if re.fullmatch(r"[+-]?\d+", lexema) or re.fullmatch(r"[+-]?(?:\d+\.\d+|\.\d+)", lexema):
        return "NUMERO", True

    if re.fullmatch(r"'(?:\\.|[^'\\])'", lexema):
        return "CARACTERE", True

    if re.fullmatch(r'"(?:\\.|[^"\\])*"', lexema):
        return "TEXTO", True

    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", lexema):
        return "NOMEVARIAVEL", True

    if lexema == "=":
        return "OP_ATRIB", True

    if lexema == ",":
        return "VG", True

    if lexema == ";":
        return "PV", True

    return "NAO_RECONHECIDO", False


def tokenizar_linha(linha: str, numero_linha: int) -> List[Token]:
    """Gera a lista de tokens da linha preservando posição e coluna."""
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


def analisar_declaracao(tokens: List[Token]) -> ResultadoSintatico:
    """
    Analisa sintaticamente conforme a gramática:
        Declara -> [TIPO] ItemDeclara [PV] | [TIPO] ItemDeclara DeclaraMultiplo [PV]
        DeclaraMultiplo -> [VG] ItemDeclara | [VG] ItemDeclara DeclaraMultiplo
        ItemDeclara -> [NOMEVARIAVEL] | [NOMEVARIAVEL] [OP_ATRIB] [VALOR]
    """
    if not tokens:
        return ResultadoSintatico(
            aceito=False,
            tipo=None,
            declaradores=[],
            mensagem="Linha vazia.",
        )

    # 1. Verifica se inicia com [TIPO]
    tipo = tokens[0].tipo
    if tipo not in set(TIPOS.values()):
        return ResultadoSintatico(
            aceito=False,
            tipo=None,
            declaradores=[],
            mensagem=f"Esperado [TIPO], mas encontrado '{tokens[0].lexema}'.",
        )

    indice = 1
    declaradores: List[Declarador] = []

    # 2. Processa os itens da declaração (ItemDeclara e DeclaraMultiplo)
    while True:
        # Espera [NOMEVARIAVEL]
        if indice >= len(tokens) or tokens[indice].tipo != "NOMEVARIAVEL":
            encontrado = tokens[indice].lexema if indice < len(tokens) else "fim da linha"
            return ResultadoSintatico(
                aceito=False,
                tipo=tipo,
                declaradores=declaradores,
                mensagem=f"Esperado [NOMEVARIAVEL], mas encontrado '{encontrado}'.",
            )

        nome = tokens[indice].lexema
        indice += 1
        valor: Optional[str] = None

        # Trata inicialização opcional: [OP_ATRIB] [VALOR]
        if indice < len(tokens) and tokens[indice].tipo == "OP_ATRIB":
            indice += 1
            if indice >= len(tokens) or tokens[indice].tipo not in TIPOS_DE_VALOR:
                encontrado = tokens[indice].lexema if indice < len(tokens) else "fim da linha"
                return ResultadoSintatico(
                    aceito=False,
                    tipo=tipo,
                    declaradores=declaradores,
                    mensagem=(
                        f"Esperado [VALOR] após '=' para '{nome}', "
                        f"mas encontrado '{encontrado}'."
                    ),
                )
            valor = tokens[indice].lexema
            indice += 1

        declaradores.append(Declarador(nome=nome, valor=valor))

        if indice >= len(tokens):
            return ResultadoSintatico(
                aceito=False,
                tipo=tipo,
                declaradores=declaradores,
                mensagem="Esperado [PV] (';') antes do fim da linha.",
            )

        # Trata múltiplos identificadores separados por [VG] (',')
        if tokens[indice].tipo == "VG":
            indice += 1
            continue

        break

    # 3. Verifica o encerramento com [PV] (';')
    if tokens[indice].tipo != "PV":
        return ResultadoSintatico(
            aceito=False,
            tipo=tipo,
            declaradores=declaradores,
            mensagem=f"Esperado [PV] (';'), mas encontrado '{tokens[indice].lexema}'.",
        )

    # 4. Assegura que não existam tokens sobressalentes após o ponto e vírgula
    if indice != len(tokens) - 1:
        encontrado = tokens[indice + 1].lexema
        return ResultadoSintatico(
            aceito=False,
            tipo=tipo,
            declaradores=declaradores,
            mensagem=f"Tokens extras não permitidos após o ponto e vírgula: '{encontrado}'.",
        )

    qtd_inicializadas = sum(item.valor is not None for item in declaradores)
    return ResultadoSintatico(
        aceito=True,
        tipo=tipo,
        declaradores=declaradores,
        mensagem=(
            f"Sintaxe correta: {len(declaradores)} variável(is) declarada(s) "
            f"com {qtd_inicializadas} inicialização(ões)."
        ),
    )


def criar_tabela_simbolos(caminho_csv: str) -> None:
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow(
            ["ID", "Token", "Tipo", "Linha", "Coluna"]
        )


def adicionar_simbolo(caminho_csv: str, identificador: int, token: Token) -> None:
    with open(caminho_csv, "a", newline="", encoding="utf-8-sig") as arquivo:
        csv.writer(arquivo, delimiter=";", lineterminator="\n").writerow(
            [identificador, token.lexema, token.tipo, token.linha, token.coluna]
        )


def mostrar_tokens(tokens: List[Token]) -> None:
    for token in tokens:
        status = "OK" if token.aceito else "ERRO"
        print(f"    [{status}] {token.lexema!r:<12} -> {token.tipo} (Linha {token.linha}, Col {token.coluna})")


def mostrar_declaracao(resultado: ResultadoSintatico) -> None:
    status = "ACEITA" if resultado.aceito else "REJEITADA"
    regra = "DECLARA_MULTIPLO" if len(resultado.declaradores) > 1 else "DECLARA"

    print(f"  [SINTÁTICO: {status} ({regra})]")
    if resultado.tipo:
        print(f"    Tipo: {resultado.tipo}")
    if resultado.declaradores:
        itens = [
            f"{d.nome} = {d.valor}" if d.valor is not None else d.nome
            for d in resultado.declaradores
        ]
        print(f"    Variáveis: {', '.join(itens)}")
    print(f"    Detalhes: {resultado.mensagem}")


def processar_arquivo(caminho_entrada: str, caminho_csv: str) -> None:
    criar_tabela_simbolos(caminho_csv)
    proximo_id = 1

    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            linha_limpa = linha.strip()
            if not linha_limpa:
                continue

            print(f"\n--- Processando Linha {numero_linha}: {linha_limpa} ---")
            tokens = tokenizar_linha(linha, numero_linha)
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

    # Cria um input.c de exemplo caso o arquivo não exista
    if not os.path.exists(caminho_entrada):
        with open(caminho_entrada, "w", encoding="utf-8") as f:
            f.write("int x = 10;\n")
            f.write("float nota = 8.5, peso;\n")
            f.write("char letra = 'A', separador;\n")
            f.write("boolean flag = true, ativo = false;\n")
            f.write("double total = x, saldo = 1500.75;\n")
            f.write("int a = ;\n")  # Exemplo com erro sintático proposital

    processar_arquivo(caminho_entrada, caminho_csv)
    print(f"\nProcessamento concluído. Tabela salva em: {caminho_csv}")


if __name__ == "__main__":
    main()