"""
Análise sintática de declarações de variáveis por máquina de estados.

Etapas
  1. Léxico: input.c -> tokens (lexema, tipo, linha, coluna) + tabela_simbolos.csv
  2. Sintático: cada declaração é avaliada token a token por um autômato
     (estado, classe do token) -> próximo estado. Se não existe transição, o
     erro lista exatamente o que era esperado naquele estado.
     Após um erro, a análise ressincroniza no próximo ';' ou no próximo tipo.

Uso: python analisador.py [arquivo.c]
"""
import csv
import os
import sys
from dataclasses import dataclass
from typing import List, Optional

PASTA = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- léxico

RESERVADAS = {
    "int": "PR:INT", "char": "PR:CHAR", "float": "PR:FLOAT",
    "double": "PR:DOUBLE", "void": "PR:VOID", "boolean": "PR:BOOLEAN",
    "true": "PR:TRUE", "false": "PR:FALSE",
}
PONTUACAO = {"=": "ATRIBUICAO", ",": "VIRGULA", ";": "PONTO_VIRGULA"}


@dataclass
class Token:
    lexema: str
    tipo: str
    linha: int
    coluna: int


def varrer(texto: str) -> List[Token]:
    toks: List[Token] = []
    for nl, linha in enumerate(texto.splitlines(), start=1):
        i, n = 0, len(linha)
        while i < n:
            c, col = linha[i], i + 1
            anterior = toks[-1].tipo if toks else None

            if c.isspace():
                i += 1
            elif c.isalpha() or c == "_":
                j = i
                while j < n and (linha[j].isalnum() or linha[j] == "_"):
                    j += 1
                p = linha[i:j]
                toks.append(Token(p, RESERVADAS.get(p, "NOMEVARIAVEL"), nl, col))
                i = j
            elif c.isdigit() or (c in "+-" and anterior == "ATRIBUICAO"
                                 and i + 1 < n and linha[i + 1].isdigit()):
                j = i + 1 if c in "+-" else i
                while j < n and linha[j].isdigit():
                    j += 1
                tipo = "INTEIRO"
                if j + 1 < n and linha[j] == "." and linha[j + 1].isdigit():
                    j += 1
                    while j < n and linha[j].isdigit():
                        j += 1
                    tipo = "FRACIONARIO"
                toks.append(Token(linha[i:j], tipo, nl, col))
                i = j
            elif c in ("'", '"'):
                j = i + 1
                while j < n and linha[j] != c:
                    j += 2 if linha[j] == "\\" else 1
                if j >= n:
                    toks.append(Token(linha[i:], "LITERAL_NAO_FECHADO", nl, col))
                    i = n
                    continue
                corpo = linha[i + 1:j]
                if c == '"':
                    tipo = "LITERAL_TEXTO"
                elif len(corpo) == 1 or (len(corpo) == 2 and corpo[0] == "\\"):
                    tipo = "LITERAL_CARACTERE"
                else:
                    tipo = "CARACTERE_INVALIDO"
                toks.append(Token(linha[i:j + 1], tipo, nl, col))
                i = j + 1
            elif c in PONTUACAO:
                toks.append(Token(c, PONTUACAO[c], nl, col))
                i += 1
            else:
                toks.append(Token(c, "DESCONHECIDO", nl, col))
                i += 1
    return toks


# ------------------------------------------------------------ sintático

# classe do token usada pelo autômato
def classe(t: Token) -> str:
    if t.tipo in ("PR:INT", "PR:CHAR", "PR:FLOAT", "PR:DOUBLE", "PR:VOID", "PR:BOOLEAN"):
        return "TIPO"
    return {
        "NOMEVARIAVEL": "NOME", "ATRIBUICAO": "ATRIB", "VIRGULA": "VG",
        "PONTO_VIRGULA": "PV",
        "INTEIRO": "VALOR", "FRACIONARIO": "VALOR", "PR:TRUE": "VALOR",
        "PR:FALSE": "VALOR", "LITERAL_CARACTERE": "VALOR", "LITERAL_TEXTO": "VALOR",
    }.get(t.tipo, "OUTRO")


DESCRICAO = {"TIPO": "um tipo", "NOME": "nome de variável", "ATRIB": "'='",
             "VALOR": "um valor", "VG": "','", "PV": "';'"}

# (estado, classe) -> próximo estado
TRANSICOES = {
    ("INICIO", "TIPO"): "APOS_TIPO",
    ("APOS_TIPO", "NOME"): "APOS_NOME",
    ("APOS_NOME", "ATRIB"): "APOS_ATRIB",
    ("APOS_NOME", "VG"): "APOS_VG",
    ("APOS_NOME", "PV"): "FIM",
    ("APOS_ATRIB", "VALOR"): "APOS_VALOR",
    ("APOS_VALOR", "VG"): "APOS_VG",
    ("APOS_VALOR", "PV"): "FIM",
    ("APOS_VG", "NOME"): "APOS_NOME",
}

# tipo da declaração -> tipos de token aceitos como valor
ACEITA = {
    "PR:INT": {"INTEIRO"},
    "PR:FLOAT": {"FRACIONARIO", "INTEIRO"},
    "PR:DOUBLE": {"FRACIONARIO", "INTEIRO"},
    "PR:CHAR": {"LITERAL_CARACTERE"},
    "PR:BOOLEAN": {"PR:TRUE", "PR:FALSE"},
    "PR:VOID": set(),
}


class ErroSintatico(Exception):
    def __init__(self, msg: str, indice: int, exibir: Optional[int] = None):
        super().__init__(msg)
        self.indice = indice  # índice do token onde o erro foi detectado
        self.exibir = indice if exibir is None else exibir  # token usado para mostrar a posição


@dataclass
class Declarador:
    nome: Token
    valor: Optional[Token] = None


@dataclass
class Declaracao:
    tipo: Token
    declaradores: List[Declarador]
    fim: Token


def esperados(estado: str) -> str:
    opcoes = [DESCRICAO[c] for (e, c) in TRANSICOES if e == estado]
    return " ou ".join(opcoes)


def avaliar(toks: List[Token], ini: int):
    """Roda o autômato a partir de toks[ini]. Retorna (Declaracao, próximo índice)."""
    estado, i = "INICIO", ini
    tipo_decl: Optional[Token] = None
    decls: List[Declarador] = []

    while estado != "FIM":
        if i >= len(toks):
            raise ErroSintatico(f"fim do arquivo inesperado; esperado {esperados(estado)}",
                                len(toks))
        t = toks[i]
        cl = classe(t)

        if t.tipo == "LITERAL_NAO_FECHADO":
            raise ErroSintatico(f"literal sem aspas de fechamento: {t.lexema}", i)
        if t.tipo == "CARACTERE_INVALIDO":
            raise ErroSintatico(
                f"{t.lexema} não é um caractere válido (use exatamente um caractere)", i)

        if (estado, cl) not in TRANSICOES:
            if estado == "INICIO":
                raise ErroSintatico(f"declaração deve começar por um tipo, encontrado '{t.lexema}'", i)
            if i > ini and t.linha > toks[i - 1].linha:
                # o que faltou deveria estar no fim da linha anterior
                raise ErroSintatico(
                    f"esperado {esperados(estado)} no fim da linha "
                    f"(a próxima linha começa com '{t.lexema}')", i, exibir=i - 1)
            raise ErroSintatico(f"esperado {esperados(estado)}, encontrado '{t.lexema}'", i)

        if estado == "APOS_NOME" and cl == "ATRIB" and tipo_decl.tipo == "PR:VOID":
            raise ErroSintatico("variável void não pode ser inicializada", i)
        if estado == "APOS_ATRIB" and t.tipo not in ACEITA[tipo_decl.tipo]:
            aceitos = " ou ".join(sorted(ACEITA[tipo_decl.tipo]))
            raise ErroSintatico(
                f"valor incompatível com {tipo_decl.lexema}: esperado {aceitos}, "
                f"encontrado {t.tipo} {t.lexema}", i)

        # ações semânticas simples para montar a árvore
        if cl == "TIPO":
            tipo_decl = t
        elif cl == "NOME":
            decls.append(Declarador(t))
        elif cl == "VALOR":
            decls[-1].valor = t

        estado = TRANSICOES[(estado, cl)]
        i += 1

    return Declaracao(tipo_decl, decls, toks[i - 1]), i


def ressincronizar(toks: List[Token], inicio: int, erro: int) -> int:
    """Descarta tokens até depois de um ';' ou antes do próximo tipo."""
    i = max(erro, inicio + 1) if erro < len(toks) else len(toks)
    if erro < len(toks) and classe(toks[erro]) == "TIPO" and erro > inicio:
        return erro
    while i < len(toks):
        if toks[i].tipo == "PONTO_VIRGULA":
            return i + 1
        if classe(toks[i]) == "TIPO":
            return i
        i += 1
    return i


# ---------------------------------------------------------------- saída

def desenhar(rotulo: str, filhos=(), prefixo="", ultimo=True, raiz=True) -> List[str]:
    if raiz:
        linhas = [rotulo]
    else:
        linhas = [prefixo + ("└── " if ultimo else "├── ") + rotulo]
        prefixo += "    " if ultimo else "│   "
    for k, (r, f) in enumerate(filhos):
        linhas += desenhar(r, f, prefixo, k == len(filhos) - 1, raiz=False)
    return linhas


def arvore(d: Declaracao) -> List[str]:
    folha = lambda t, nome: (f"[{nome}] {t.lexema}", ())
    lista = []
    for k, dc in enumerate(d.declaradores):
        sub = [folha(dc.nome, "NOMEVARIAVEL")]
        if dc.valor:
            sub.append(("Inicializacao", (
                ("[ATRIBUICAO] =", ()), folha(dc.valor, "VALOR:" + dc.valor.tipo))))
        lista.append(("Declarador", tuple(sub)))
        if k < len(d.declaradores) - 1:
            lista.append(("[VG] ,", ()))
    filhos = ((f"[TIPO] {d.tipo.lexema}", ()), ("ListaDeclarador", tuple(lista)),
              ("[PV] ;", ()))
    return desenhar("Declaracao", filhos)


def salvar_csv(toks: List[Token], caminho: str) -> None:
    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";", lineterminator="\n")
        w.writerow(["ID", "token", "tipo", "linha", "coluna"])
        for k, t in enumerate(toks, start=1):
            w.writerow([k, t.lexema, t.tipo, t.linha, t.coluna])


def main() -> None:
    entrada = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PASTA, "input.c")
    with open(entrada, encoding="utf-8") as f:
        texto = f.read()
    linhas_fonte = texto.splitlines()
    toks = varrer(texto)
    salvar_csv(toks, os.path.join(PASTA, "tabela_simbolos.csv"))

    print(f"Arquivo: {os.path.basename(entrada)}  ({len(toks)} tokens)")
    resumo, i = [], 0
    while i < len(toks):
        ini = i
        try:
            decl, i = avaliar(toks, ini)
            trecho = " ".join(t.lexema for t in toks[ini:i])
            print(f"\n[ACEITA]   linha {toks[ini].linha}: {trecho}")
            for l in arvore(decl):
                print("   " + l)
            resumo.append((toks[ini].linha, "ACEITA", ""))
        except ErroSintatico as e:
            prox = ressincronizar(toks, ini, e.indice)
            alvo = toks[min(e.exibir, len(toks) - 1)]
            print(f"\n[REJEITADA] linha {alvo.linha}: {linhas_fonte[alvo.linha - 1].strip()}")
            print(f"   {e} (coluna {alvo.coluna})")
            resumo.append((alvo.linha, "REJEITADA", str(e)))
            i = prox

    ok = sum(1 for r in resumo if r[1] == "ACEITA")
    print("\n" + "=" * 60)
    for linha, st, msg in resumo:
        print(f"  linha {linha:<3} {st:<10} {msg}")
    print("=" * 60)
    print(f"Resumo: {ok} aceita(s), {len(resumo) - ok} rejeitada(s).")


if __name__ == "__main__":
    main()
