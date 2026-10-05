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

PALAVRAS_RESERVADAS = {
    "if": "PR:IF",
    "else": "PR:ELSE",
    "while": "PR:WHILE",
    "for": "PR:FOR",
    "return": "PR:RETURN",
}

VALORES_BOOLEANOS = {
    "true": "BOOLEANO",
    "false": "BOOLEANO",
}

TIPOS_DE_VALOR = {
    "NUMERO",
    "CARACTERE",
    "TEXTO",
    "BOOLEANO",
    "NOMEVARIAVEL",
}

DELIMITADORES = {
    "(": "AP",
    ")": "FP",
    "{": "AC",
    "}": "FC",
    "[": "ACOL",
    "]": "FCOL",
}

PARES_FECHAMENTO = {
    ")": "(",
    "}": "{",
    "]": "[",
}


PADRAO_TOKEN = re.compile(
    r'"(?:\\.|[^"\\])*"'           
    r"|'(?:\\.|[^'\\])'"           
    r"|[+-]?(?:\d+\.\d+|\.\d+)"    
    r"|[+-]?\d+"                   
    r"|[A-Za-z_][A-Za-z0-9_]*"     
    r"|==|<=|>=|!="                
    r"|[,;=<>!(){}\[\]]"           
    r"|[^\s]"                      
)


@dataclass
class Token:
    id_token: int
    lexema: str
    tipo: str
    linha: int
    coluna: int
    ref: Optional[int] = None
    aceito: bool = True


class ErroSintatico(Exception):
    pass


def classificar_lexema(lexema: str) -> Tuple[str, bool]:
    if lexema in TIPOS:
        return TIPOS[lexema], True

    if lexema in PALAVRAS_RESERVADAS:
        return PALAVRAS_RESERVADAS[lexema], True

    if lexema in VALORES_BOOLEANOS:
        return VALORES_BOOLEANOS[lexema], True

    if lexema in DELIMITADORES:
        return DELIMITADORES[lexema], True

    if lexema in {">", "<", "==", "!=", "<=", ">="}:
        return "SINAL_COMPARACAO", True

    if lexema == "=":
        return "ATRIBUICAO", True

    if lexema == ",":
        return "VG", True

    if lexema == ";":
        return "PV", True

    if re.fullmatch(r"[+-]?\d+", lexema) or re.fullmatch(r"[+-]?(?:\d+\.\d+|\.\d+)", lexema):
        return "NUMERO", True

    if re.fullmatch(r"'(?:\\.|[^'\\])'", lexema):
        return "CARACTERE", True

    if re.fullmatch(r'"(?:\\.|[^"\\])*"', lexema):
        return "TEXTO", True

    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", lexema):
        return "NOMEVARIAVEL", True

    return "NAO_RECONHECIDO", False


def tokenizar_arquivo(caminho_entrada: str) -> Tuple[List[Token], List[str]]:
    tokens: List[Token] = []
    pilha_delimitadores = []
    erros_lexicos = []
    id_atual = 1

    with open(caminho_entrada, "r", encoding="utf-8") as arq:
        for num_linha, linha in enumerate(arq, start=1):
            for match in PADRAO_TOKEN.finditer(linha):
                lexema = match.group(0)
                coluna = match.start() + 1
                tipo, aceito = classificar_lexema(lexema)

                tok = Token(
                    id_token=id_atual,
                    lexema=lexema,
                    tipo=tipo,
                    linha=num_linha,
                    coluna=coluna,
                    aceito=aceito,
                )

                if lexema in {"(", "{", "["}:
                    pilha_delimitadores.append((lexema, id_atual, num_linha, coluna))
                elif lexema in PARES_FECHAMENTO:
                    abertura_esperada = PARES_FECHAMENTO[lexema]
                    if not pilha_delimitadores:
                        erros_lexicos.append(
                            f"[Linha {num_linha}, Col {coluna}] Fechamento '{lexema}' sem abertura correspondente."
                        )
                    else:
                        topo_simbolo, topo_id, topo_lin, topo_col = pilha_delimitadores.pop()
                        if topo_simbolo != abertura_esperada:
                            erros_lexicos.append(
                                f"[Linha {num_linha}, Col {coluna}] Fechamento '{lexema}' incompatível com '{topo_simbolo}' "
                                f"(aberto na Linha {topo_lin}, Col {topo_col}, ID {topo_id})."
                            )
                        else:
                            tok.ref = topo_id

                tokens.append(tok)
                id_atual += 1

    while pilha_delimitadores:
        simb, id_ab, lin_ab, col_ab = pilha_delimitadores.pop()
        erros_lexicos.append(
            f"[Linha {lin_ab}, Col {col_ab}] Delimitador '{simb}' (ID {id_ab}) não foi fechado até o fim do arquivo."
        )

    return tokens, erros_lexicos


class AnalisadorSintatico:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def token_atual(self) -> Optional[Token]:
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def casar(self, tipo_esperado: str) -> Token:
        tok = self.token_atual()
        if tok is None:
            raise ErroSintatico(
                f"Fim inesperado do arquivo. Era esperado token do tipo '{tipo_esperado}'."
            )
        if tok.tipo != tipo_esperado:
            raise ErroSintatico(
                f"[Linha {tok.linha}, Col {tok.coluna}] Erro sintático: "
                f"esperado '{tipo_esperado}', mas encontrado '{tok.tipo}' ({tok.lexema!r})."
            )
        self.pos += 1
        return tok

    def analisar_programa(self) -> None:
        self.lista_comandos()
        if self.pos < len(self.tokens):
            tok = self.token_atual()
            raise ErroSintatico(
                f"[Linha {tok.linha}, Col {tok.coluna}] Token inesperado fora de comando: {tok.lexema!r}."
            )

    def lista_comandos(self) -> None:
        tipos_inicio_comando = set(TIPOS.values()) | {"PR:IF", "NOMEVARIAVEL"}
        while self.token_atual() is not None and self.token_atual().tipo in tipos_inicio_comando:
            self.comando()

    def comando(self) -> None:
        tok = self.token_atual()
        if tok is None:
            return

        if tok.tipo in set(TIPOS.values()):
            self.declara()
        elif tok.tipo == "PR:IF":
            self.se()
        elif tok.tipo == "NOMEVARIAVEL":
            self.atribuicao()
        else:
            raise ErroSintatico(
                f"[Linha {tok.linha}, Col {tok.coluna}] Comando inválido iniciado por '{tok.lexema}'."
            )

    def se(self) -> None:
        self.casar("PR:IF")
        self.casar("AP")
        self.condicao()
        self.casar("FP")
        self.bloco()

    def bloco(self) -> None:
        self.casar("AC")
        self.lista_comandos()
        self.casar("FC")

    def condicao(self) -> None:
        self.valor()
        self.casar("SINAL_COMPARACAO")
        self.valor()

    def atribuicao(self) -> None:
        self.casar("NOMEVARIAVEL")
        self.casar("ATRIBUICAO")
        self.valor()
        self.casar("PV")

    def declara(self) -> None:
        tok_tipo = self.token_atual()
        if tok_tipo and tok_tipo.tipo in set(TIPOS.values()):
            self.pos += 1
        else:
            encontrado = tok_tipo.tipo if tok_tipo else "fim de arquivo"
            raise ErroSintatico(f"Esperado [TIPO], encontrado '{encontrado}'.")

        self.item_declara()

        while self.token_atual() and self.token_atual().tipo == "VG":
            self.casar("VG")
            self.item_declara()

        self.casar("PV")

    def item_declara(self) -> None:
        self.casar("NOMEVARIAVEL")
        if self.token_atual() and self.token_atual().tipo == "ATRIBUICAO":
            self.casar("ATRIBUICAO")
            self.valor()

    def valor(self) -> Token:
        tok = self.token_atual()
        if tok and tok.tipo in TIPOS_DE_VALOR:
            self.pos += 1
            return tok

        encontrado = tok.tipo if tok else "fim de arquivo"
        raise ErroSintatico(
            f"[Linha {tok.linha if tok else '?'}] Esperado [VALOR], mas encontrado '{encontrado}'."
        )


def salvar_tabela_simbolos(tokens: List[Token], caminho_csv: str) -> None:
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as arq:
        escritor = csv.writer(arq, delimiter=";", lineterminator="\n")
        escritor.writerow(["ID", "Token", "Tipo", "Linha", "Coluna", "Ref"])
        for t in tokens:
            escritor.writerow([
                t.id_token,
                t.lexema,
                t.tipo,
                t.linha,
                t.coluna,
                t.ref if t.ref is not None else "",
            ])


def main() -> None:
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_input = os.path.join(diretorio, "input.c")
    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")

    if not os.path.exists(caminho_input):
        print(f"Erro: Arquivo '{caminho_input}' não encontrado.")
        return

    tokens, erros_delimitadores = tokenizar_arquivo(caminho_input)

    salvar_tabela_simbolos(tokens, caminho_csv)
    print(f"Tabela de símbolos salva em: {caminho_csv}")

    if erros_delimitadores:
        print("\nErros de delimitadores:")
        for erro in erros_delimitadores:
            print(f"  ❌ {erro}")
    else:
        print("Delimitadores (), {} e [] devidamente balanceados e referenciados.")

    print("\nExecutando análise sintática...")
    parser = AnalisadorSintatico(tokens)
    try:
        parser.analisar_programa()
        print("Código aceito com sucesso pela gramática.")
    except ErroSintatico as e:
        print(f"Erro sintático: {e}")


if __name__ == "__main__":
    main()