"""
Scanner + verificador de delimitadores + tabela de símbolos.

Regras:
  * ( ), { } e [ ] devem ter contagem idêntica de abre e fecha.
  * Na tabela de símbolos, cada token de fechamento traz na coluna Ref o ID
    do token de abertura ao qual ele se refere.

Uso: python verificador_delimitadores.py [arquivo.c]
"""

import csv
import os
import sys
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Dict, List, Optional

# ----------------------------------------------------------------------------
# Definições léxicas
# ----------------------------------------------------------------------------

PALAVRAS_RESERVADAS = {
    "int": "PR:INT", "char": "PR:CHAR", "float": "PR:FLOAT",
    "double": "PR:DOUBLE", "void": "PR:VOID", "boolean": "PR:BOOLEAN",
    "true": "PR:TRUE", "false": "PR:FALSE", "if": "PR:IF", "else": "PR:ELSE",
}

# símbolo -> (nome do token, família, símbolo par)
DELIMITADORES = {
    "(": ("ABRE_PARENTESE", "PARENTESE", ")"),
    ")": ("FECHA_PARENTESE", "PARENTESE", "("),
    "{": ("ABRE_CHAVE", "CHAVE", "}"),
    "}": ("FECHA_CHAVE", "CHAVE", "{"),
    "[": ("ABRE_COLCHETE", "COLCHETE", "]"),
    "]": ("FECHA_COLCHETE", "COLCHETE", "["),
}
ABRES = {"(", "{", "["}
FECHAS = {")", "}", "]"}

SIMPLES = {",": "VIRGULA", ";": "PONTO_VIRGULA", "=": "ATRIBUICAO",
           "+": "OPERADOR_ARITMETICO", "-": "OPERADOR_ARITMETICO",
           "*": "OPERADOR_ARITMETICO", "/": "OPERADOR_ARITMETICO",
           "<": "SINAL_COMPARACAO", ">": "SINAL_COMPARACAO"}
DUPLOS = {"==", "!=", "<=", ">="}


@dataclass
class Simbolo:
    id: int
    lexema: str
    tipo: str
    linha: int
    coluna: int
    valido: bool = True
    ref: Optional[int] = None  # só preenchido em fechamentos


# ----------------------------------------------------------------------------
# Scanner manual (sem regex)
# ----------------------------------------------------------------------------

class Scanner:
    def __init__(self, texto: str):
        self.texto = texto
        self.pos = 0
        self.linha = 1
        self.col = 1
        self.simbolos: List[Simbolo] = []

    def _atual(self) -> str:
        return self.texto[self.pos] if self.pos < len(self.texto) else ""

    def _espiar(self, n: int = 1) -> str:
        i = self.pos + n
        return self.texto[i] if i < len(self.texto) else ""

    def _avancar(self) -> str:
        c = self.texto[self.pos]
        self.pos += 1
        if c == "\n":
            self.linha += 1
            self.col = 1
        else:
            self.col += 1
        return c

    def _emitir(self, lexema, tipo, linha, col, valido=True):
        self.simbolos.append(
            Simbolo(len(self.simbolos) + 1, lexema, tipo, linha, col, valido)
        )

    def _ler_literal(self, aspa: str) -> None:
        linha, col = self.linha, self.col
        buf = [self._avancar()]
        fechou = False
        while self._atual() and self._atual() != "\n":
            c = self._avancar()
            buf.append(c)
            if c == "\\" and self._atual() and self._atual() != "\n":
                buf.append(self._avancar())
            elif c == aspa:
                fechou = True
                break
        tipo = "LITERAL_TEXTO" if aspa == '"' else "LITERAL_CARACTERE"
        if not fechou:
            tipo = "LITERAL_NAO_FECHADO"
        self._emitir("".join(buf), tipo, linha, col, fechou)

    def _ler_numero(self) -> None:
        linha, col = self.linha, self.col
        buf = []
        while self._atual().isdigit():
            buf.append(self._avancar())
        tipo = "INTEIRO"
        if self._atual() == "." and self._espiar().isdigit():
            tipo = "FRACIONARIO"
            buf.append(self._avancar())
            while self._atual().isdigit():
                buf.append(self._avancar())
        self._emitir("".join(buf), tipo, linha, col)

    def _ler_palavra(self) -> None:
        linha, col = self.linha, self.col
        buf = []
        while self._atual().isalnum() or self._atual() == "_":
            buf.append(self._avancar())
        palavra = "".join(buf)
        self._emitir(palavra, PALAVRAS_RESERVADAS.get(palavra, "NOMEVARIAVEL"),
                     linha, col)

    def varrer(self) -> List[Simbolo]:
        while self._atual():
            c = self._atual()
            if c.isspace():
                self._avancar()
            elif c in ('"', "'"):
                self._ler_literal(c)
            elif c.isdigit():
                self._ler_numero()
            elif c.isalpha() or c == "_":
                self._ler_palavra()
            elif c in DELIMITADORES:
                linha, col = self.linha, self.col
                self._avancar()
                self._emitir(c, DELIMITADORES[c][0], linha, col)
            elif c + self._espiar() in DUPLOS:
                linha, col = self.linha, self.col
                lex = self._avancar() + self._avancar()
                self._emitir(lex, "SINAL_COMPARACAO", linha, col)
            elif c in SIMPLES:
                linha, col = self.linha, self.col
                self._avancar()
                self._emitir(c, SIMPLES[c], linha, col)
            else:
                linha, col = self.linha, self.col
                self._avancar()
                self._emitir(c, "NAO_RECONHECIDO", linha, col, False)
        return self.simbolos


# ----------------------------------------------------------------------------
# Verificador de delimitadores
# ----------------------------------------------------------------------------

@dataclass
class RelatorioDelimitadores:
    # família -> {"abre": n, "fecha": n}
    contagem: Dict[str, Dict[str, int]] = field(default_factory=OrderedDict)
    erros: List[str] = field(default_factory=list)
    pares: int = 0

    @property
    def balanceado(self) -> bool:
        return not self.erros and all(
            c["abre"] == c["fecha"] for c in self.contagem.values()
        )


def verificar_delimitadores(simbolos: List[Simbolo]) -> RelatorioDelimitadores:
    """
    Duas verificações:
      1) contagem por família (abre == fecha);
      2) pareamento com pilha, preenchendo Simbolo.ref nos fechamentos.

    Em caso de erro o verificador continua (recuperação), de modo que todos os
    problemas sejam listados de uma vez.
    """
    rel = RelatorioDelimitadores()
    for fam in ("PARENTESE", "CHAVE", "COLCHETE"):
        rel.contagem[fam] = {"abre": 0, "fecha": 0}

    pilha: List[Simbolo] = []

    def onde(s: Simbolo) -> str:
        return f"'{s.lexema}' (ID {s.id}, linha {s.linha}, coluna {s.coluna})"

    for s in simbolos:
        if s.lexema in ABRES:
            rel.contagem[DELIMITADORES[s.lexema][1]]["abre"] += 1
            pilha.append(s)
        elif s.lexema in FECHAS:
            familia = DELIMITADORES[s.lexema][1]
            rel.contagem[familia]["fecha"] += 1
            esperado = DELIMITADORES[s.lexema][2]

            # procura, de cima para baixo, a abertura correspondente
            idx = next((i for i in range(len(pilha) - 1, -1, -1)
                        if pilha[i].lexema == esperado), None)

            if idx is None:
                rel.erros.append(f"Fechamento {onde(s)} sem abertura correspondente.")
                continue

            # tudo que está acima de idx ficou sem fechar
            for orfao in reversed(pilha[idx + 1:]):
                rel.erros.append(
                    f"Abertura {onde(orfao)} não foi fechada antes de {onde(s)}."
                )
            s.ref = pilha[idx].id
            rel.pares += 1
            del pilha[idx:]

    for orfao in reversed(pilha):
        rel.erros.append(f"Abertura {onde(orfao)} sem fechamento correspondente.")

    # Diferença de contagem só é mencionada se ainda não explicada acima
    for fam, c in rel.contagem.items():
        if c["abre"] != c["fecha"] and not rel.erros:
            rel.erros.append(
                f"Contagem de {fam} diferente: {c['abre']} abre x {c['fecha']} fecha."
            )
    return rel


# ----------------------------------------------------------------------------
# Saída
# ----------------------------------------------------------------------------

COLUNAS = ["ID", "token", "tipo", "linha", "coluna", "Ref"]


def linha_tabela(s: Simbolo) -> List:
    return [s.id, s.lexema, s.tipo, s.linha, s.coluna,
            s.ref if s.ref is not None else ""]


def salvar_csv(simbolos: List[Simbolo], caminho: str) -> None:
    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";", lineterminator="\n")
        w.writerow(COLUNAS)
        for s in simbolos:
            if s.valido:
                w.writerow(linha_tabela(s))


def imprimir_tabela(simbolos: List[Simbolo]) -> None:
    linhas = [[str(x) for x in linha_tabela(s)] for s in simbolos if s.valido]
    larg = [max(len(COLUNAS[i]), *(len(l[i]) for l in linhas)) if linhas
            else len(COLUNAS[i]) for i in range(len(COLUNAS))]
    sep = "+" + "+".join("-" * (w + 2) for w in larg) + "+"
    fmt = lambda cols: "| " + " | ".join(c.ljust(w) for c, w in zip(cols, larg)) + " |"
    print(sep)
    print(fmt(COLUNAS))
    print(sep)
    for l in linhas:
        print(fmt(l))
    print(sep)


def imprimir_relatorio(rel: RelatorioDelimitadores) -> None:
    print("CONTAGEM DE DELIMITADORES")
    for fam, c in rel.contagem.items():
        marca = "OK " if c["abre"] == c["fecha"] else "ERRO"
        print(f"  [{marca}] {fam:<9} abre={c['abre']:<3} fecha={c['fecha']:<3}")
    print()
    if rel.balanceado:
        print(f"RESULTADO: BALANCEADO ({rel.pares} par(es) validado(s)).")
    else:
        print("RESULTADO: NÃO BALANCEADO")
        for e in rel.erros:
            print(f"  - {e}")


def main() -> None:
    base = os.path.dirname(os.path.abspath(__file__))
    entrada = sys.argv[1] if len(sys.argv) > 1 else os.path.join(base, "input.c")
    saida = os.path.join(base, "tabela_simbolos.csv")

    with open(entrada, "r", encoding="utf-8") as f:
        texto = f.read()

    simbolos = Scanner(texto).varrer()
    relatorio = verificar_delimitadores(simbolos)

    print(f"Arquivo: {os.path.basename(entrada)}\n")
    imprimir_relatorio(relatorio)
    print("\nTABELA DE SÍMBOLOS")
    imprimir_tabela(simbolos)

    rejeitados = [s for s in simbolos if not s.valido]
    if rejeitados:
        print("\nTOKENS REJEITADOS")
        for s in rejeitados:
            print(f"  {s.lexema!r} ({s.tipo}) linha {s.linha}, coluna {s.coluna}")

    salvar_csv(simbolos, saida)
    print(f"\nCSV salvo em: {saida}")


if __name__ == "__main__":
    main()
