"""
Analisador Sintático - declaração com inicialização - Romeo Noro Guterres

Etapas:
  1. Léxico: transforma input.c em uma lista de tokens (tipo, lexema, linha, coluna)
     e grava tabela_simbolos.csv.
  2. Sintático: descida recursiva seguindo a gramática de sintaxe.txt.
     Para cada declaração aceita é exibida a árvore de derivação; para cada
     declaração rejeitada é exibido o erro, e a análise continua a partir do
     próximo ';' (recuperação em modo pânico).

Uso: python analisador_sintatico.py [arquivo.c]
"""
import csv
import os
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))

PALAVRAS_RESERVADAS = {
    "int": "PR:INT", "char": "PR:CHAR", "float": "PR:FLOAT",
    "double": "PR:DOUBLE", "void": "PR:VOID", "boolean": "PR:BOOLEAN",
    "true": "PR:TRUE", "false": "PR:FALSE",
}
SIMBOLOS = {"=": "SATR", ",": "VG", ";": "PV"}


# ----------------------------------------------------------------- léxico

class Token:
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo, self.lexema, self.linha, self.coluna = tipo, lexema, linha, coluna

    def __repr__(self):
        return f"{self.tipo}({self.lexema!r}) {self.linha}:{self.coluna}"


def analisar_lexico(fonte):
    tokens = []
    for num_linha, linha in enumerate(fonte.splitlines(), start=1):
        i, n = 0, len(linha)
        while i < n:
            c = linha[i]
            col = i + 1

            if c.isspace():
                i += 1

            elif c.isalpha() or c == "_":
                j = i
                while j < n and (linha[j].isalnum() or linha[j] == "_"):
                    j += 1
                palavra = linha[i:j]
                tokens.append(Token(PALAVRAS_RESERVADAS.get(palavra, "NOMEVARIAVEL"),
                                    palavra, num_linha, col))
                i = j

            elif c.isdigit() or (c in "+-" and i + 1 < n and linha[i + 1].isdigit()):
                j = i + 1
                while j < n and linha[j].isdigit():
                    j += 1
                tipo = "INTEIRO"
                if j + 1 < n and linha[j] == "." and linha[j + 1].isdigit():
                    j += 1
                    while j < n and linha[j].isdigit():
                        j += 1
                    tipo = "FRACIONARIO"
                tokens.append(Token(tipo, linha[i:j], num_linha, col))
                i = j

            elif c == "'":
                # 'x' vira ASPAS CARACTER ASPAS, como na gramática do professor
                tokens.append(Token("ASPAS", "'", num_linha, col))
                if i + 2 < n and linha[i + 2] == "'":
                    tokens.append(Token("CARACTER", linha[i + 1], num_linha, col + 1))
                    tokens.append(Token("ASPAS", "'", num_linha, col + 2))
                    i += 3
                else:
                    i += 1

            elif c in SIMBOLOS:
                tokens.append(Token(SIMBOLOS[c], c, num_linha, col))
                i += 1

            else:
                tokens.append(Token("DESCONHECIDO", c, num_linha, col))
                i += 1
    return tokens


# -------------------------------------------------------------- sintático

class ErroSintatico(Exception):
    def __init__(self, mensagem, token):
        onde = f"linha {token.linha}, coluna {token.coluna}" if token else "fim do arquivo"
        super().__init__(f"{mensagem} ({onde})")


class No:
    def __init__(self, rotulo, filhos=None):
        self.rotulo = rotulo
        self.filhos = filhos or []

    def imprimir(self, prefixo="", ultimo=True, raiz=True):
        if raiz:
            print(self.rotulo)
        else:
            print(prefixo + ("└── " if ultimo else "├── ") + self.rotulo)
            prefixo += "    " if ultimo else "│   "
        for k, filho in enumerate(self.filhos):
            filho.imprimir(prefixo, k == len(self.filhos) - 1, raiz=False)


def folha(token):
    return No(f"[{token.tipo}] {token.lexema}" if not token.tipo.startswith("PR:")
              else f"{token.tipo} {token.lexema}")


# Para cada tipo: (não terminal da declaração, da lista, do item,
#                  valores aceitos na inicialização ou None se não aceita)
REGRAS_TIPO = {
    "PR:INT":     ("DeclaraInt",  "ListaInt",  "ItemInt",  {"INTEIRO"}),
    "PR:FLOAT":   ("DeclaraFrac", "ListaFrac", "ItemFrac", {"FRACIONARIO", "INTEIRO"}),
    "PR:DOUBLE":  ("DeclaraFrac", "ListaFrac", "ItemFrac", {"FRACIONARIO", "INTEIRO"}),
    "PR:CHAR":    ("DeclaraChar", "ListaChar", "ItemChar", {"CHAR"}),
    "PR:BOOLEAN": ("DeclaraBool", "ListaBool", "ItemBool", {"PR:TRUE", "PR:FALSE"}),
    "PR:VOID":    ("DeclaraVoid", "ListaVoid", None,       None),
}


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self, tipo_esperado, descricao=None):
        tok = self.atual()
        if tok is None or tok.tipo != tipo_esperado:
            achou = f"'{tok.lexema}'" if tok else "fim do arquivo"
            raise ErroSintatico(f"esperado {descricao or tipo_esperado}, encontrado {achou}", tok)
        self.pos += 1
        return tok

    # Declara -> DeclaraInt | DeclaraFrac | DeclaraChar | DeclaraBool | DeclaraVoid
    def declara(self):
        tok = self.atual()
        if tok.tipo not in REGRAS_TIPO:
            raise ErroSintatico(f"esperado um tipo (int, char, float, double, void, boolean), "
                                f"encontrado '{tok.lexema}'", tok)
        nt_decl, nt_lista, nt_item, valores = REGRAS_TIPO[tok.tipo]
        self.pos += 1

        tipo_no = folha(tok)
        if nt_decl == "DeclaraFrac":
            tipo_no = No("TipoFrac", [tipo_no])

        filhos = [tipo_no, self.item(nt_item, valores)]
        if self.atual() and self.atual().tipo == "VG":
            filhos.append(self.lista(nt_lista, nt_item, valores))
        filhos.append(folha(self.consumir("PV", "';'")))
        return No("Declara", [No(nt_decl, filhos)])

    # ListaX -> [VG] ItemX | [VG] ItemX ListaX
    def lista(self, nt_lista, nt_item, valores):
        filhos = [folha(self.consumir("VG")), self.item(nt_item, valores)]
        if self.atual() and self.atual().tipo == "VG":
            filhos.append(self.lista(nt_lista, nt_item, valores))
        return No(nt_lista, filhos)

    # ItemX -> [NOMEVARIAVEL] | [NOMEVARIAVEL][SATR] valor
    def item(self, nt_item, valores):
        nome = folha(self.consumir("NOMEVARIAVEL", "nome de variável"))
        tok = self.atual()
        if tok is None or tok.tipo != "SATR":
            return nome if nt_item is None else No(nt_item, [nome])

        if valores is None:
            raise ErroSintatico("variável void não pode ser inicializada", tok)
        filhos = [nome, folha(self.consumir("SATR"))]
        filhos.append(self.valor(nt_item, valores))
        return No(nt_item, filhos)

    def valor(self, nt_item, valores):
        tok = self.atual()
        if tok is None:
            raise ErroSintatico("esperado valor após '='", tok)

        if "CHAR" in valores:
            if tok.tipo != "ASPAS":
                raise ErroSintatico(f"char deve receber um caractere entre aspas simples, "
                                    f"encontrado '{tok.lexema}'", tok)
            return No("Caractere", [folha(self.consumir("ASPAS")),
                                    folha(self.consumir("CARACTER", "um caractere")),
                                    folha(self.consumir("ASPAS", "aspas de fechamento"))])

        if tok.tipo not in valores:
            esperado = " ou ".join(sorted(valores))
            raise ErroSintatico(f"valor incompatível com o tipo: esperado {esperado}, "
                                f"encontrado {tok.tipo} '{tok.lexema}'", tok)
        self.pos += 1
        if nt_item == "ItemFrac":
            return No("ValorFrac", [folha(tok)])
        if nt_item == "ItemBool":
            return No("ValorBool", [folha(tok)])
        return folha(tok)

    def sincronizar(self, inicio):
        """Modo pânico: descarta tokens até depois do próximo ';' ou até o
        início de uma nova declaração (um tipo), o que vier primeiro."""
        self.pos = max(self.pos, inicio + 1)
        while self.atual() and self.atual().tipo not in REGRAS_TIPO:
            if self.atual().tipo == "PV":
                self.pos += 1
                return
            self.pos += 1

    def analisar(self):
        aceitas, erros = 0, 0
        while self.atual():
            inicio = self.pos
            linha = self.atual().linha
            try:
                arvore = self.declara()
                trecho = " ".join(t.lexema for t in self.tokens[inicio:self.pos])
                print(f"\n[OK]   linha {linha}: {trecho}")
                arvore.imprimir()
                aceitas += 1
            except ErroSintatico as e:
                self.sincronizar(inicio)
                trecho = " ".join(t.lexema for t in self.tokens[inicio:self.pos])
                print(f"\n[ERRO] linha {linha}: {trecho}\n       {e}")
                erros += 1
        return aceitas, erros


# ------------------------------------------------------------------- main

def main():
    entrada = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PASTA, "input.c")
    with open(entrada, encoding="utf-8") as arq:
        tokens = analisar_lexico(arq.read())

    with open(os.path.join(PASTA, "tabela_simbolos.csv"), "w", encoding="utf-8", newline="") as arq:
        escritor = csv.writer(arq, delimiter=";")
        escritor.writerow(["ID", "token", "tipo", "linha", "coluna"])
        for k, t in enumerate(tokens, start=1):
            escritor.writerow([k, t.lexema, t.tipo, t.linha, t.coluna])

    aceitas, erros = Parser(tokens).analisar()
    print(f"\nResumo: {aceitas} declaração(ões) aceita(s), {erros} com erro.")


if __name__ == "__main__":
    main()
