class NoArvore:

    def __init__(self, nome):
        self.nome = nome
        self.filhos = []

    def adicionar(self, filho):
        self.filhos.append(filho)



def leitura_config(nome_arquivo):
    with open(nome_arquivo,"r",encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]
    
    #Estados
    estados =  linhas[0].strip().split()
    estado_inicial = estados[0]

    #Simbolos
    alfabeto = set(linhas[1].strip().split())

    #Estados finais
    finais = {}

    for item in linhas[2].strip().split():
        estado, token = item.split(":")
        finais[estado] = token

    #Transições
    transicoes = {}

    for linha in linhas[3:]:
        for regra in linha.strip().split():

            origem, simbolo, destino = regra.split(":")

            transicoes[(origem,simbolo)] = destino

    return estado_inicial, alfabeto, finais, transicoes


def reconhecer(texto, inicio, alfabeto, finais, transicoes):

    estado = inicio
    ultimo_estado_final = None
    ultimo_indice = -1

    for indice, caractere in enumerate(texto):

        if caractere not in alfabeto:
            break

        chave = (estado, caractere)

        if chave not in transicoes:
            break

        estado = transicoes[chave]

        if estado in finais:

            ultimo_estado_final = estado
            ultimo_indice = indice

    if ultimo_estado_final is None:
        return None;

    token = texto[:ultimo_indice + 1]
    tipo = finais[ultimo_estado_final]

    return token, tipo, ultimo_indice + 1

def analisar(nome_arquivo, inicio, alfabeto, finais, transicoes):

    tabela = []
    identificador = 1

    tipos_dados = {
        "int": "INTEIRO",
        "char": "CARACTERE",
        "float": "FRACIONÁRIO",
        "double": "FRACIONÁRIO",
        "boolean": "BOOLEAN"
    }

    valores_booleanos = {
        "true": "BOOLEAN",
        "false": "BOOLEAN"
    }

    tipo_atual = None
    esperando_valor = False

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:

        for numero_linha, linha in enumerate(arquivo, start=1):

            posicao = 0

            while posicao < len(linha):

                if linha[posicao].isspace():
                    posicao += 1
                    continue

                resultado = reconhecer(
                    linha[posicao:],
                    inicio,
                    alfabeto,
                    finais,
                    transicoes
                )

                if resultado is None:

                    tabela.append({
                        "ID": identificador,
                        "token": linha[posicao],
                        "tipo": "ERRO_LEXICO",
                        "linha": numero_linha,
                        "coluna": posicao
                    })

                    identificador += 1
                    posicao += 1

                else:

                    token, tipo, quantidade = resultado

                    if tipo == "NOMEVARIAVEL":

                        if token in tipos_dados:
                            tipo = "PR:" + tipos_dados[token]
                            tipo_atual = tipos_dados[token]

                        elif token in valores_booleanos:
                            tipo = "BOOLEAN"

                    if token == "=":
                        esperando_valor = True

                    elif esperando_valor:

                        tipo_valor = tipo

                        if tipo_atual == "INTEIRO":

                            if tipo_valor != "INTEIRO":
                                tipo = "ERRO_TIPO"

                        elif tipo_atual == "FRACIONÁRIO":

                            if tipo_valor not in ["INTEIRO", "FRACIONÁRIO"]:
                                tipo = "ERRO_TIPO"

                        elif tipo_atual == "BOOLEAN":

                            if tipo_valor != "BOOLEAN":
                                tipo = "ERRO_TIPO"

                        esperando_valor = False

                    if token == ";":
                        tipo_atual = None
                        esperando_valor = False

                    tabela.append({
                        "ID": identificador,
                        "token": token,
                        "tipo": tipo,
                        "linha": numero_linha,
                        "coluna": posicao
                    })

                    identificador += 1
                    posicao += quantidade

    return tabela

def mostrar_tabela(tabela):

    largura = 86

    print()
    print("╔" + "═" * largura + "╗")
    print("║" + " " * 25 + "ANALISADOR LÉXICO" + " " * 43 + "║")
    print("║" + " " * 23 + "TABELA DE SÍMBOLOS" + " " * 44 + "║")
    print("╠" + "═" * largura + "╣")

    print(
        "║ "
        f"{'ID':<5}"
        f"{'TOKEN':<25}"
        f"{'TIPO':<25}"
        f"{'LINHA':<10}"
        f"{'COLUNA':<10}"
        "║"
    )

    print("╠" + "═" * largura + "╣")

    for item in tabela:

        if item["tipo"] == "ERRO_LEXICO":
            marcador = "⚠"
        elif item["tipo"] == "ERRO_TIPO":
            marcador = "✖"
        else:
            marcador = " "

        print(
            "║ "
            f"{marcador}"
            f"{item['ID']:<4}"
            f"{item['token']:<25}"
            f"{item['tipo']:<25}"
            f"{item['linha']:<10}"
            f"{item['coluna']:<10}"
            "║"
        )

    print("╚" + "═" * largura + "╝")
    print()

def criar_arvore(tabela):

    raiz = NoArvore("PROGRAMA")

    declaracoes = NoArvore("DECLARACOES")
    raiz.adicionar(declaracoes)

    inicio = 0

    while inicio < len(tabela):

        fim = inicio

        while fim < len(tabela) and tabela[fim]["token"] != ";":
            fim += 1

        if fim < len(tabela):
            fim += 1

        tokens = tabela[inicio:fim]

        if not tokens:
            break

        declaracao = NoArvore("DECLARACAO")

        for item in tokens:

            token = item["token"]
            tipo = item["tipo"]

            if tipo.startswith("PR:"):

                no_tipo = NoArvore("TIPO")
                no_tipo.adicionar(NoArvore(token))
                declaracao.adicionar(no_tipo)

            elif tipo == "NOMEVARIAVEL":

                no_id = NoArvore("IDENTIFICADOR")
                no_id.adicionar(NoArvore(token))
                declaracao.adicionar(no_id)

            elif tipo == "ATRIBUICAO":

                no_atribuicao = NoArvore("ATRIBUICAO")
                no_atribuicao.adicionar(NoArvore("="))
                declaracao.adicionar(no_atribuicao)

            elif tipo == "INTEIRO":

                no_valor = NoArvore("VALOR")

                no_inteiro = NoArvore("INTEIRO")
                no_inteiro.adicionar(NoArvore(token))

                no_valor.adicionar(no_inteiro)
                declaracao.adicionar(no_valor)

            elif tipo == "FRACIONÁRIO":

                no_valor = NoArvore("VALOR")

                no_fracionario = NoArvore("FRACIONÁRIO")
                no_fracionario.adicionar(NoArvore(token))

                no_valor.adicionar(no_fracionario)
                declaracao.adicionar(no_valor)

            elif tipo == "CARACTERE":

                no_valor = NoArvore("VALOR")

                no_caractere = NoArvore("CARACTERE")
                no_caractere.adicionar(NoArvore(token))

                no_valor.adicionar(no_caractere)
                declaracao.adicionar(no_valor)

            elif tipo == "BOOLEAN":

                no_valor = NoArvore("VALOR")

                no_boolean = NoArvore("BOOLEAN")
                no_boolean.adicionar(NoArvore(token))

                no_valor.adicionar(no_boolean)
                declaracao.adicionar(no_valor)

            elif tipo == "VIRGULA":

                no_virgula = NoArvore("VIRGULA")
                no_virgula.adicionar(NoArvore(","))
                declaracao.adicionar(no_virgula)

            elif tipo == "PONTO_VIRGULA":

                no_ponto = NoArvore("PONTO_VIRGULA")
                no_ponto.adicionar(NoArvore(";"))
                declaracao.adicionar(no_ponto)

        declaracoes.adicionar(declaracao)

        inicio = fim

    return raiz

def mostrar_arvore(no, prefixo="", ultimo=True, raiz=True):

    if raiz:
        print(no.nome)
    else:
        simbolo = "└── " if ultimo else "├── "
        print(prefixo + simbolo + no.nome)

    if raiz:
        novo_prefixo = ""
    else:
        novo_prefixo = prefixo + ("    " if ultimo else "│   ")

    for i, filho in enumerate(no.filhos):

        ultimo_filho = i == len(no.filhos) - 1

        mostrar_arvore(
            filho,
            novo_prefixo,
            ultimo_filho,
            False
        )

def leitura_sintaxe(nome_arquivo):

    regras = {}

    with open(nome_arquivo, "r", encoding="utf-8") as arquivo:

        for linha in arquivo:

            linha = linha.strip()

            if not linha:
                continue

            if "->" not in linha:
                continue

            esquerda, direita = linha.split("->", 1)

            esquerda = esquerda.strip()
            direita = direita.strip()

            if esquerda not in regras:
                regras[esquerda] = []

            regras[esquerda].append(direita.split())

    return regras



def main():

    config = "configAFD.md"
    fonte = "input.c"
    sintaxe = "sintaxe.txt"

    inicio, alfabeto, finais, transicoes = leitura_config(config)

    tabela = analisar(
        fonte,
        inicio,
        alfabeto,
        finais,
        transicoes
    )

    regras = leitura_sintaxe(sintaxe)

    mostrar_tabela(tabela)

    arvore = criar_arvore(tabela)

    print()
    print("╔" + "═" * 38 + "╗")
    print("║" + " " * 8 + "ÁRVORE DE DERIVAÇÃO" + " " * 10 + "║")
    print("╚" + "═" * 38 + "╝")
    print()

    mostrar_arvore(arvore)


main()
