"""
Analisador Léxico com AFD configurável - Romeo Noro Guterres

O AFD é carregado de configAfd.md:
  1a linha: estados (o primeiro é o estado inicial)
  2a linha: símbolos do alfabeto
  3a linha: estados finais no formato Estado:RECONHECE
  4a linha em diante: transições no formato Origem:simbolo:Destino

Cada linha de numeros.txt contém um termo a ser reconhecido.
O resultado é impresso na tela e gravado em tabela_simbolos.csv.

Uso: python analisador.py [config] [entrada]
"""
import csv
import os
import sys

PASTA = os.path.dirname(os.path.abspath(__file__))


class AFD:
    def __init__(self, caminho_config):
        with open(caminho_config, encoding="utf-8") as arq:
            linhas = [l.strip() for l in arq if l.strip()]

        if len(linhas) < 3:
            raise ValueError("configAfd.md incompleto: são necessárias ao menos 3 linhas")

        self.estados = linhas[0].split()
        self.estado_inicial = self.estados[0]
        self.simbolos = set(linhas[1].split())

        # Estado -> nome do token reconhecido
        self.finais = {}
        for item in linhas[2].split():
            estado, reconhece = item.split(":", 1)
            self.finais[estado] = reconhece

        # (estado, simbolo) -> próximo estado
        # rsplit/split com limite trata símbolos como ':' sem quebrar a regra
        self.transicoes = {}
        for linha in linhas[3:]:
            for regra in linha.split():
                origem, resto = regra.split(":", 1)
                simbolo, destino = resto.rsplit(":", 1)
                self.transicoes[(origem, simbolo)] = destino

    def reconhecer(self, termo):
        """Percorre o AFD caractere a caractere.
        Retorna o tipo do token ou uma mensagem de erro."""
        estado = self.estado_inicial
        for pos, c in enumerate(termo):
            if c not in self.simbolos:
                return f"ERRO: símbolo '{c}' não pertence ao alfabeto"
            proximo = self.transicoes.get((estado, c))
            if proximo is None:
                return f"ERRO: sem transição de {estado} com '{c}' (posição {pos + 1})"
            estado = proximo

        if estado in self.finais:
            return self.finais[estado]
        return f"ERRO: terminou no estado {estado}, que não é final"


def main():
    config = sys.argv[1] if len(sys.argv) > 1 else os.path.join(PASTA, "configAfd.md")
    entrada = sys.argv[2] if len(sys.argv) > 2 else os.path.join(PASTA, "numeros.txt")

    afd = AFD(config)

    tabela = []
    with open(entrada, encoding="utf-8") as arq:
        for num_linha, linha in enumerate(arq, start=1):
            termo = linha.strip()
            if not termo:
                continue
            resultado = afd.reconhecer(termo)
            print(f"{termo:<15} -> {resultado}")
            if not resultado.startswith("ERRO"):
                coluna = linha.index(termo) + 1
                tabela.append([len(tabela) + 1, termo, resultado, num_linha, coluna])

    saida = os.path.join(PASTA, "tabela_simbolos.csv")
    with open(saida, "w", encoding="utf-8", newline="") as arq:
        escritor = csv.writer(arq, delimiter=";")
        escritor.writerow(["ID", "token", "tipo", "linha", "coluna"])
        escritor.writerows(tabela)
    print(f"\nTabela de símbolos gravada em {saida}")


if __name__ == "__main__":
    main()
