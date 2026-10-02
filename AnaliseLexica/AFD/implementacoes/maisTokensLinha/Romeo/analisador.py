"""
Analisador Léxico com AFD - vários tokens por linha - Romeo Noro Guterres

Lê o AFD de AFD_config.txt, percorre input.c linha por linha e, como os
tokens estão separados por espaço em branco, cada vez que encontra um espaço
o reconhecimento termina e o AFD volta ao estado inicial para o próximo token.

Gera tabela_simbolos.csv com as colunas: ID, token, tipo, linha e coluna.
Tokens rejeitados pelo AFD são listados como erro léxico (com linha/coluna)
e não entram na tabela.

Uso: python analisador.py [AFD_config.txt] [input.c]
"""
import csv
import os
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))


class AFD:
    def __init__(self, caminho_config):
        with open(caminho_config, encoding="utf-8") as arq:
            linhas = [l.strip() for l in arq if l.strip()]

        self.estados = linhas[0].split()
        self.estado_inicial = self.estados[0]
        self.simbolos = set(linhas[1].split())
        self.finais = dict(item.split(":", 1) for item in linhas[2].split())

        self.transicoes = {}
        for linha in linhas[3:]:
            for regra in linha.split():
                origem, resto = regra.split(":", 1)
                simbolo, destino = resto.rsplit(":", 1)
                self.transicoes[(origem, simbolo)] = destino

    def reconhecer(self, termo):
        """Retorna (tipo, None) se aceito ou (None, motivo) se rejeitado."""
        estado = self.estado_inicial
        for c in termo:
            if c not in self.simbolos:
                return None, f"símbolo '{c}' não pertence ao alfabeto"
            estado = self.transicoes.get((estado, c))
            if estado is None:
                return None, f"sem transição para '{c}'"
        if estado not in self.finais:
            return None, f"parou no estado {estado}, que não é final"
        return self.finais[estado], None


def separar_tokens(linha):
    """Varre a linha caractere a caractere guardando a coluna (base 1) onde
    cada token começa. Espaço/tab encerra o token atual."""
    tokens = []
    atual, inicio = "", 0
    for col, c in enumerate(linha, start=1):
        if c in " \t\r\n":
            if atual:
                tokens.append((atual, inicio))
                atual = ""
        else:
            if not atual:
                inicio = col
            atual += c
    if atual:
        tokens.append((atual, inicio))
    return tokens


def analisar(afd, caminho_entrada):
    tabela, erros = [], []
    with open(caminho_entrada, encoding="utf-8") as arq:
        for num_linha, linha in enumerate(arq, start=1):
            for token, coluna in separar_tokens(linha):
                tipo, motivo = afd.reconhecer(token)
                if tipo:
                    tabela.append((len(tabela) + 1, token, tipo, num_linha, coluna))
                else:
                    erros.append((token, num_linha, coluna, motivo))
    return tabela, erros


def main():
    config = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PASTA, "AFD_config.txt")
    entrada = sys.argv[2] if len(sys.argv) > 2 else os.path.join(PASTA, "input.c")

    afd = AFD(config)
    tabela, erros = analisar(afd, entrada)

    print(f"{'ID':>3}  {'TOKEN':<12} {'TIPO':<18} {'LINHA':>5} {'COLUNA':>6}")
    for id_, token, tipo, linha, coluna in tabela:
        print(f"{id_:>3}  {token:<12} {tipo:<18} {linha:>5} {coluna:>6}")

    if erros:
        print("\nErros léxicos:")
        for token, linha, coluna, motivo in erros:
            print(f"  '{token}' (linha {linha}, coluna {coluna}): {motivo}")

    saida = os.path.join(PASTA, "tabela_simbolos.csv")
    with open(saida, "w", encoding="utf-8", newline="") as arq:
        escritor = csv.writer(arq, delimiter=";")
        escritor.writerow(["ID", "token", "tipo", "linha", "coluna"])
        escritor.writerows(tabela)
    print(f"\nTabela de símbolos gravada em {saida}")


if __name__ == "__main__":
    main()
