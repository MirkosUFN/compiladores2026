"""
Analisador Léxico e Sintático - Balanceamento de Delimitadores ( ), { } e [ ]
Autor: Gabriel Teixeira (Compiladores - Prof. Mirkos)

Objetivos do Exercício 2:
  1. Contagem Idêntica: O número de abre parênteses '(' deve ser igual ao de fecha parênteses ')'.
     O mesmo para chaves '{ }' e colchetes '[ ]'.
  2. Análise com Pilha (Autômato com Pilha): Cada fechamento deve casar com a abertura correspondente mais recente.
  3. Tabela de Símbolos: A coluna 'Ref' de cada token de fechamento deve referenciar o 'ID' do token de abertura correspondente.

Uso:
  python analisador_sintatico.py [arquivo_fonte.c]
"""

import csv
import os
import sys

# Configuração de suporte UTF-8 no terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PASTA_ATUAL = os.path.dirname(os.path.abspath(__file__))

# Palavras Reservadas da linguagem
PALAVRAS_RESERVADAS = {
    "int": "PR:INT",
    "char": "PR:CHAR",
    "float": "PR:FLOAT",
    "double": "PR:DOUBLE",
    "void": "PR:VOID",
    "boolean": "PR:BOOLEAN",
    "true": "PR:TRUE",
    "false": "PR:FALSE",
    "if": "PR:IF",
    "else": "PR:ELSE",
    "while": "PR:WHILE",
    "for": "PR:FOR",
    "return": "PR:RETURN",
}

# Mapeamento de delimitadores (lexema -> tipo do token)
ABERTURAS = {
    "(": "AP",   # Abre Parênteses
    "{": "ACH",  # Abre Chaves
    "[": "ACO",  # Abre Colchetes
}

FECHAMENTOS = {
    ")": "FP",   # Fecha Parênteses
    "}": "FCH",  # Fecha Chaves
    "]": "FCO",  # Fecha Colchetes
}

# Relação de correspondência: Fechamento -> Abertura esperada
PAR_DE = {
    "FP": "AP",
    "FCH": "ACH",
    "FCO": "ACO",
}

# Nomes descritivos para mensagens de erro
NOMES_DELIMITADORES = {
    "AP": "parêntese '('",
    "ACH": "chave '{'",
    "ACO": "colchete '['",
    "FP": "parêntese ')'",
    "FCH": "chave '}'",
    "FCO": "colchete ']'",
}

# Operadores de dois caracteres
OPERADORES_DUPLOS = {
    "==": "IGUAL",
    "!=": "DIFERENTE",
    ">=": "MAIORIGUAL",
    "<=": "MENORIGUAL",
    "&&": "E",
    "||": "OU",
    "++": "INCREMENTO",
    "--": "DECREMENTO",
}

# Símbolos terminais simples
SIMBOLOS = {
    "=": "SATR",
    ",": "VG",
    ";": "PV",
    ">": "MAIOR",
    "<": "MENOR",
    "+": "SOMA",
    "-": "SUB",
    "*": "MULT",
    "/": "DIV",
    "!": "NAO",
    **ABERTURAS,
    **FECHAMENTOS,
}


# ==============================================================================
# 1. ANÁLISE LÉXICA
# ==============================================================================

class Token:
    def __init__(self, id_, tipo, lexema, linha, coluna):
        self.id = id_
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna
        self.ref = None  # Preenchido exclusivamente nos tokens de fechamento

    def __repr__(self):
        ref_str = f" Ref={self.ref}" if self.ref is not None else ""
        return f"Token({self.id}, {self.tipo}, '{self.lexema}', {self.linha}:{self.coluna}{ref_str})"


def analisar_lexico(codigo_fonte):
    """
    Realiza o escaneamento léxico do código fonte.
    Identifica tokens, rastreia coordenadas de linha e coluna e ignora comentários.
    """
    tokens = []

    def adicionar_token(tipo, lexema, linha, coluna):
        id_ = len(tokens) + 1
        tokens.append(Token(id_, tipo, lexema, linha, coluna))

    linhas = codigo_fonte.splitlines()

    for num_linha, linha in enumerate(linhas, start=1):
        i = 0
        n = len(linha)

        while i < n:
            c = linha[i]
            coluna = i + 1

            # Espaços em branco
            if c.isspace():
                i += 1
                continue

            # Comentários de linha única (//)
            if linha.startswith("//", i):
                break

            # Identificadores e Palavras Reservadas
            if c.isalpha() or c == "_":
                j = i
                while j < n and (linha[j].isalnum() or linha[j] == "_"):
                    j += 1
                palavra = linha[i:j]
                tipo = PALAVRAS_RESERVADAS.get(palavra, "NOMEVARIAVEL")
                adicionar_token(tipo, palavra, num_linha, coluna)
                i = j

            # Literais Numéricos (Inteiros ou Fracionários)
            elif c.isdigit():
                j = i
                while j < n and linha[j].isdigit():
                    j += 1
                tipo = "INTEIRO"
                if j + 1 < n and linha[j] == "." and linha[j + 1].isdigit():
                    j += 1
                    while j < n and linha[j].isdigit():
                        j += 1
                    tipo = "FRACIONARIO"
                adicionar_token(tipo, linha[i:j], num_linha, coluna)
                i = j

            # Literal de Caractere: 'c'
            elif c == "'" and i + 2 < n and linha[i + 2] == "'":
                adicionar_token("CARACTER", linha[i:i + 3], num_linha, coluna)
                i += 3

            # Literal de String: "texto"
            elif c == '"':
                j = linha.find('"', i + 1)
                j = n if j == -1 else j + 1
                adicionar_token("TEXTO", linha[i:j], num_linha, coluna)
                i = j

            # Operadores duplos (==, !=, <=, >=, etc.)
            elif linha[i:i + 2] in OPERADORES_DUPLOS:
                adicionar_token(OPERADORES_DUPLOS[linha[i:i + 2]], linha[i:i + 2], num_linha, coluna)
                i += 2

            # Símbolos e Delimitadores simples
            elif c in SIMBOLOS:
                adicionar_token(SIMBOLOS[c], c, num_linha, coluna)
                i += 1

            # Caracteres não reconhecidos
            else:
                adicionar_token("DESCONHECIDO", c, num_linha, coluna)
                i += 1

    return tokens


# ==============================================================================
# 2. ANÁLISE SINTÁTICA (VERIFICAÇÃO DE BALANCEAMENTO COM PILHA)
# ==============================================================================

def verificar_delimitadores(tokens):
    """
    Verifica o balanceamento e o aninhamento sintático dos delimitadores utilizando uma pilha.
    Para cada token de fechamento válido, preenche o atributo `tok.ref` com o ID da abertura correspondente.
    Retorna uma lista de strings com os erros encontrados.
    """
    pilha = []
    erros = []

    for tok in tokens:
        # 1. Delimitador de Abertura: Empilha
        if tok.tipo in NOMES_DELIMITADORES and tok.tipo in PAR_DE.values():
            pilha.append(tok)

        # 2. Delimitador de Fechamento: Desempilha e valida
        elif tok.tipo in PAR_DE:
            abertura_esperada = PAR_DE[tok.tipo]

            # Caso de erro: fechamento sem nenhuma abertura prévia
            if not pilha:
                erros.append(
                    f"Linha {tok.linha}, Coluna {tok.coluna}: '{tok.lexema}' (ID {tok.id}) "
                    f"fecha {NOMES_DELIMITADORES[tok.tipo]} que nunca foi aberto."
                )
                continue

            topo = pilha[-1]

            # Casamento perfeito: tipos correspondem
            if topo.tipo == abertura_esperada:
                pilha.pop()
                tok.ref = topo.id  # Preenche a referência com o ID do token de abertura
            else:
                # Erro de cruzamento de blocos ou aninhamento invertido
                erros.append(
                    f"Linha {tok.linha}, Coluna {tok.coluna}: '{tok.lexema}' (ID {tok.id}) "
                    f"inesperado. Esperado fechamento de '{topo.lexema}' (ID {topo.id}, Linha {topo.linha}, Coluna {topo.coluna})."
                )

    # 3. Delimitadores que restaram na pilha (nunca foram fechados)
    for tok in pilha:
        erros.append(
            f"Linha {tok.linha}, Coluna {tok.coluna}: '{tok.lexema}' (ID {tok.id}) "
            f"aberto mas nunca foi fechado até o fim do arquivo."
        )

    return erros


def contar_delimitadores(tokens):
    """
    Calcula a contagem total de aberturas e fechamentos de cada delimitador.
    Retorna um dicionário com as tuplas: (total_aberturas, total_fechamentos).
    """
    contagem = {}
    pares = [
        ("Parênteses ( )", "(", ")"),
        ("Chaves { }", "{", "}"),
        ("Colchetes [ ]", "[", "]"),
    ]

    for nome, abre, fecha in pares:
        total_abre = sum(1 for t in tokens if t.lexema == abre)
        total_fecha = sum(1 for t in tokens if t.lexema == fecha)
        contagem[nome] = (total_abre, total_fecha)

    return contagem


# ==============================================================================
# 3. EXPORTAÇÃO DA TABELA DE SÍMBOLOS
# ==============================================================================

def gravar_tabela_simbolos(tokens, caminho_csv):
    """
    Exporta a tabela de símbolos para CSV com delimitador ';' e a coluna 'Ref'.
    """
    with open(caminho_csv, "w", encoding="utf-8", newline="") as arq:
        escritor = csv.writer(arq, delimiter=";")
        escritor.writerow(["ID", "token", "tipo", "linha", "coluna", "Ref"])
        for t in tokens:
            escritor.writerow([
                t.id,
                t.lexema,
                t.tipo,
                t.linha,
                t.coluna,
                "" if t.ref is None else t.ref,
            ])


# ==============================================================================
# 4. EXECUÇÃO PRINCIPAL
# ==============================================================================

def main():
    arquivo_entrada = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PASTA_ATUAL, "input.c")

    if not os.path.exists(arquivo_entrada):
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado.")
        sys.exit(1)

    print("=" * 65)
    print(" Analisador Sintático - Exercício 2: Balanceamento e Referência")
    print(f" Arquivo analisado: {arquivo_entrada}")
    print("=" * 65)

    with open(arquivo_entrada, "r", encoding="utf-8") as arq:
        conteudo = arq.read()

    # 1. Análise Léxica
    tokens = analisar_lexico(conteudo)

    # 2. Análise Sintática com Pilha
    erros = verificar_delimitadores(tokens)
    contagem = contar_delimitadores(tokens)

    # 3. Gravação da Tabela de Símbolos
    nome_base = os.path.splitext(os.path.basename(arquivo_entrada))[0]
    nome_saida = "tabela_simbolos.csv" if nome_base == "input" else f"tabela_simbolos_{nome_base}.csv"
    caminho_saida = os.path.join(PASTA_ATUAL, nome_saida)
    gravar_tabela_simbolos(tokens, caminho_saida)

    # 4. Exibição dos Delimitadores Reconhecidos
    print(f"\n[+] Total de tokens reconhecidos: {len(tokens)}")
    print("\n--- DELIMITADORES IDENTIFICADOS E REFERÊNCIAS ---")
    print(f"{'ID':>4}  {'Token':<8} {'Tipo':<8} {'Linha':>5} {'Coluna':>6}  {'Ref (ID de Abertura)':<20}")
    print("-" * 55)

    tokens_delimitadores = [t for t in tokens if t.tipo in ABERTURAS.values() or t.tipo in FECHAMENTOS.values()]
    for t in tokens_delimitadores:
        ref_str = str(t.ref) if t.ref is not None else "-"
        print(f"{t.id:>4}  {t.lexema:<8} {t.tipo:<8} {t.linha:>5} {t.coluna:>6}  {ref_str:<20}")

    # 5. Exibição da Contagem dos Tokens
    print("\n--- CONTAGEM DE DELIMITADORES ---")
    print(f"{'Delimitador':<18} {'Aberturas':>10} {'Fechamentos':>12}  {'Status':<10}")
    print("-" * 55)

    todas_contagens_iguais = True
    for delimitador, (abre, fecha) in contagem.items():
        status = "OK (Igual)" if abre == fecha else "DIFERENTE"
        if abre != fecha:
            todas_contagens_iguais = False
        print(f"{delimitador:<18} {abre:>10} {fecha:>12}  {status:<10}")

    # 6. Relatório Sintático Final
    print("\n--- RESULTADO DA ANÁLISE SINTÁTICA ---")
    if erros or not todas_contagens_iguais:
        print(f"[ERRO] Foram encontrados {len(erros)} problema(s) de balanceamento/aninhamento:")
        for e in erros:
            print(f"  ✖ {e}")
    else:
        print("[SUCESSO] Todos os delimitadores ( ), { } e [ ] possuem contagem idêntica,")
        print("          estão aninhados corretamente e tiveram suas referências vinculadas!")

    print(f"\n[+] Tabela de símbolos exportada em: {caminho_saida}")
    print("=" * 65)


if __name__ == "__main__":
    main()
