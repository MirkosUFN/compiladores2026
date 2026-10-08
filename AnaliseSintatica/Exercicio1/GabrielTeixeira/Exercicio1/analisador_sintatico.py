"""
Analisador Léxico e Sintático - Declaração de Variáveis com Inicialização
Autor: Gabriel Teixeira (Baseado na estrutura da disciplina de Compiladores - Prof. Mirkos)

Etapas:
  1. Análise Léxica: Converte o código-fonte em uma sequência de tokens (tipo, lexema, linha, coluna)
     e gera o arquivo tabela_simbolos.csv.
  2. Análise Sintática: Executa um parser descendente recursivo de acordo com as regras de sintaxe.txt.
     Para cada sentença válida, exibe a árvore sintática de derivação.
     Para sentenças inválidas, relata a mensagem de erro com localização e aplica recuperação em modo pânico.

Uso:
  python analisador_sintatico.py [arquivo_fonte.c]
"""

import csv
import os
import sys

# Garante suporte adequado a caracteres UTF-8 no terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Tabela de Palavras Reservadas da linguagem
PALAVRAS_RESERVADAS = {
    "int": "PR:INT",
    "char": "PR:CHAR",
    "float": "PR:FLOAT",
    "double": "PR:DOUBLE",
    "void": "PR:VOID",
    "boolean": "PR:BOOLEAN",
    "true": "PR:TRUE",
    "false": "PR:FALSE",
}

# Símbolos terminais especiais
SIMBOLOS = {
    "=": "SATR",
    ",": "VG",
    ";": "PV",
}


# ==============================================================================
# 1. ANÁLISE LÉXICA
# ==============================================================================

class Token:
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna

    def __repr__(self):
        return f"{self.tipo}('{self.lexema}') [{self.linha}:{self.coluna}]"


def analisar_lexico(codigo_fonte):
    """
    Realiza a tokenização do código-fonte.
    Ignora comentários (//) e espaços em branco.
    """
    tokens = []
    linhas = codigo_fonte.splitlines()

    for num_linha, linha in enumerate(linhas, start=1):
        i = 0
        n = len(linha)

        while i < n:
            c = linha[i]
            coluna = i + 1

            # Ignora espaços em branco e tabulações
            if c.isspace():
                i += 1
                continue

            # Ignora comentários de linha única iniciados por //
            if c == "/" and i + 1 < n and linha[i + 1] == "/":
                break

            # Identificadores e Palavras Reservadas
            if c.isalpha() or c == "_":
                j = i
                while j < n and (linha[j].isalnum() or linha[j] == "_"):
                    j += 1
                palavra = linha[i:j]
                tipo = PALAVRAS_RESERVADAS.get(palavra, "NOMEVARIAVEL")
                tokens.append(Token(tipo, palavra, num_linha, coluna))
                i = j

            # Literais Numéricos (Inteiros ou Fracionários com suporte a sinal opcional)
            elif c.isdigit() or (c in "+-" and i + 1 < n and linha[i + 1].isdigit()):
                j = i + 1
                while j < n and linha[j].isdigit():
                    j += 1
                tipo = "INTEIRO"
                # Verifica se há parte decimal (ponto seguido de dígitos)
                if j + 1 < n and linha[j] == "." and linha[j + 1].isdigit():
                    j += 1
                    while j < n and linha[j].isdigit():
                        j += 1
                    tipo = "FRACIONARIO"
                tokens.append(Token(tipo, linha[i:j], num_linha, coluna))
                i = j

            # Literal de Caractere: 'c'
            elif c == "'":
                tokens.append(Token("ASPAS", "'", num_linha, coluna))
                if i + 2 < n and linha[i + 2] == "'":
                    tokens.append(Token("CARACTER", linha[i + 1], num_linha, coluna + 1))
                    tokens.append(Token("ASPAS", "'", num_linha, coluna + 2))
                    i += 3
                else:
                    i += 1

            # Símbolos de pontuação e operadores
            elif c in SIMBOLOS:
                tokens.append(Token(SIMBOLOS[c], c, num_linha, coluna))
                i += 1

            # Caracteres não reconhecidos
            else:
                tokens.append(Token("DESCONHECIDO", c, num_linha, coluna))
                i += 1

    return tokens


# ==============================================================================
# 2. ANÁLISE SINTÁTICA
# ==============================================================================

class ErroSintatico(Exception):
    def __init__(self, mensagem, token):
        posicao = f"linha {token.linha}, coluna {token.coluna}" if token else "fim do arquivo"
        super().__init__(f"{mensagem} ({posicao})")


class NoArvore:
    """Nó para representação visual da Árvore de Derivação Sintática."""
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


def no_folha(token):
    """Cria um nó folha com a descrição legível do token terminal."""
    if token.tipo.startswith("PR:"):
        return NoArvore(f"{token.tipo} {token.lexema}")
    return NoArvore(f"[{token.tipo}] {token.lexema}")


# Mapeamento semântico-sintático para cada tipo:
# (Não-Terminal Declaração, Não-Terminal Lista, Não-Terminal Item, Conjunto de tipos de valores aceitos)
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

    def token_atual(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consumir(self, tipo_esperado, descricao=None):
        tok = self.token_atual()
        if tok is None or tok.tipo != tipo_esperado:
            encontrado = f"'{tok.lexema}'" if tok else "fim do arquivo"
            desc = descricao or tipo_esperado
            raise ErroSintatico(f"Esperado {desc}, encontrado {encontrado}", tok)
        self.pos += 1
        return tok

    # Declara -> DeclaraInt | DeclaraFrac | DeclaraChar | DeclaraBool | DeclaraVoid
    def declara(self):
        tok = self.token_atual()
        if tok is None or tok.tipo not in REGRAS_TIPO:
            encontrado = f"'{tok.lexema}'" if tok else "fim do arquivo"
            raise ErroSintatico(f"Esperado tipo de dado (int, float, double, char, boolean, void), encontrado {encontrado}", tok)

        nt_decl, nt_lista, nt_item, valores = REGRAS_TIPO[tok.tipo]
        self.pos += 1

        tipo_no = no_folha(tok)
        if nt_decl == "DeclaraFrac":
            tipo_no = NoArvore("TipoFrac", [tipo_no])

        filhos = [tipo_no, self.item(nt_item, valores)]

        # Se houver vírgula, processa repetição de variáveis (ListaX)
        if self.token_atual() and self.token_atual().tipo == "VG":
            filhos.append(self.lista(nt_lista, nt_item, valores))

        # Toda declaração finaliza obrigatoriamente com ';'
        filhos.append(no_folha(self.consumir("PV", "';' (ponto e vírgula)")))
        return NoArvore("Declara", [NoArvore(nt_decl, filhos)])

    # ListaX -> [VG] ItemX | [VG] ItemX ListaX
    def lista(self, nt_lista, nt_item, valores):
        filhos = [no_folha(self.consumir("VG", "','")), self.item(nt_item, valores)]
        if self.token_atual() and self.token_atual().tipo == "VG":
            filhos.append(self.lista(nt_lista, nt_item, valores))
        return NoArvore(nt_lista, filhos)

    # ItemX -> [NOMEVARIAVEL] | [NOMEVARIAVEL] [SATR] valor
    def item(self, nt_item, valores):
        nome = no_folha(self.consumir("NOMEVARIAVEL", "identificador da variável"))
        tok = self.token_atual()

        # Variável sem atribuição
        if tok is None or tok.tipo != "SATR":
            return nome if nt_item is None else NoArvore(nt_item, [nome])

        # Se houver atribuição em tipo void, acusa erro imediatamente
        if valores is None:
            raise ErroSintatico("Variável do tipo void não aceita inicialização de valor", tok)

        # Variável com atribuição: [NOMEVARIAVEL] [SATR] [VALOR]
        filhos = [nome, no_folha(self.consumir("SATR", "'='"))]
        filhos.append(self.valor(nt_item, valores))
        return NoArvore(nt_item, filhos)

    def valor(self, nt_item, valores):
        tok = self.token_atual()
        if tok is None:
            raise ErroSintatico("Esperado valor após operador de atribuição '='", tok)

        # Caso Char: [ASPAS] [CARACTER] [ASPAS]
        if "CHAR" in valores:
            if tok.tipo != "ASPAS":
                raise ErroSintatico(f"Variável char deve ser inicializada com caractere entre aspas simples (ex: 'a'), encontrado '{tok.lexema}'", tok)
            return NoArvore("Caractere", [
                no_folha(self.consumir("ASPAS")),
                no_folha(self.consumir("CARACTER", "um único caractere")),
                no_folha(self.consumir("ASPAS", "aspas simples de fechamento"))
            ])

        # Verificação do tipo de literal recebido
        if tok.tipo not in valores:
            esperado = " ou ".join(sorted(valores))
            raise ErroSintatico(f"Valor incompatível com o tipo: esperado {esperado}, encontrado {tok.tipo} '{tok.lexema}'", tok)

        self.pos += 1
        if nt_item == "ItemFrac":
            return NoArvore("ValorFrac", [no_folha(tok)])
        if nt_item == "ItemBool":
            return NoArvore("ValorBool", [no_folha(tok)])
        return no_folha(tok)

    def sincronizar(self, inicio):
        """
        Recuperação de Erros em Modo Pânico:
        Avança os tokens até passar do próximo ';' ou encontrar o início de uma nova declaração (tipo primitivo).
        """
        self.pos = max(self.pos, inicio + 1)
        while self.token_atual() and self.token_atual().tipo not in REGRAS_TIPO:
            if self.token_atual().tipo == "PV":
                self.pos += 1
                return
            self.pos += 1

    def analisar(self):
        """Executa a análise sintática de todo o fluxo de tokens."""
        aceitas = 0
        erros = 0

        while self.token_atual():
            inicio = self.pos
            linha = self.token_atual().linha
            try:
                arvore = self.declara()
                trecho = " ".join(t.lexema for t in self.tokens[inicio:self.pos])
                print(f"\n[OK]   Linha {linha}: {trecho}")
                arvore.imprimir()
                aceitas += 1
            except ErroSintatico as e:
                self.sincronizar(inicio)
                trecho = " ".join(t.lexema for t in self.tokens[inicio:self.pos])
                print(f"\n[ERRO] Linha {linha}: {trecho}\n       => {e}")
                erros += 1

        return aceitas, erros


# ==============================================================================
# 3. EXECUÇÃO PRINCIPAL
# ==============================================================================

def main():
    arquivo_entrada = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PASTA_ATUAL, "input.c")

    if not os.path.exists(arquivo_entrada):
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado.")
        sys.exit(1)

    print(f"============================================================")
    print(f" Analisador Sintático - Compiladores (Prof. Mirkos)")
    print(f" Arquivo analisado: {arquivo_entrada}")
    print(f"============================================================")

    with open(arquivo_entrada, "r", encoding="utf-8") as arq:
        codigo_fonte = arq.read()

    # 1. Análise Léxica
    tokens = analisar_lexico(codigo_fonte)

    # Gravação da Tabela de Símbolos em CSV
    caminho_csv = os.path.join(PASTA_ATUAL, "tabela_simbolos.csv")
    with open(caminho_csv, "w", encoding="utf-8", newline="") as arq:
        escritor = csv.writer(arq, delimiter=";")
        escritor.writerow(["ID", "token", "tipo", "linha", "coluna"])
        for k, t in enumerate(tokens, start=1):
            escritor.writerow([k, t.lexema, t.tipo, t.linha, t.coluna])

    print(f"\n[+] Tabela de símbolos gravada com sucesso em: {caminho_csv}")
    print(f"[+] Total de tokens reconhecidos: {len(tokens)}")

    # 2. Análise Sintática
    print("\nIniciando Análise Sintática...")
    parser = Parser(tokens)
    aceitas, erros = parser.analisar()

    print("\n------------------------------------------------------------")
    print(f"Resumo da Análise:")
    print(f"  ✔ Declarações aceitas: {aceitas}")
    print(f"  ✖ Declarações com erro: {erros}")
    print(f"------------------------------------------------------------")


if __name__ == "__main__":
    main()
