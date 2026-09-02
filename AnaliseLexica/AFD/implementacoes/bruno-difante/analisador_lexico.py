"""
Analisador Lexico baseado em AFD (Automato Finito Deterministico).

O automato e' inteiramente definido pelo arquivo configAfd.md, no formato:
    linha 1: estados do AFD, separados por espaco em branco
    linha 2: simbolos (alfabeto) reconhecidos pelo AFD
    linha 3: estados finais e o que reconhecem -> Estado:reconhece
    linha 4+: regras de transicao -> EstadoInicial:simbolo:EstadoFinal

Uso:
    python analisador_lexico.py [configAfd.md] [entrada.txt]

Se nenhum argumento for passado, usa "configAfd.md" e "entrada.txt" na
mesma pasta do script.
"""

import csv
import sys
from pathlib import Path


class AFD:
    def __init__(self, caminho_config: Path):
        self.estados = []
        self.estado_inicial = None
        self.simbolos = set()
        self.estados_finais = {}  # estado -> nome do token reconhecido
        self.transicoes = {}      # (estado, simbolo) -> estado_destino

        self._carregar_config(caminho_config)

    def _carregar_config(self, caminho_config: Path) -> None:
        with open(caminho_config, encoding="utf-8") as arquivo:
            linhas = [linha.strip() for linha in arquivo if linha.strip()]

        if len(linhas) < 3:
            raise ValueError("configAfd.md precisa ter ao menos 3 linhas (estados, simbolos, finais)")

        # 1a linha: estados
        self.estados = linhas[0].split()
        self.estado_inicial = self.estados[0]

        # 2a linha: simbolos reconhecidos
        self.simbolos = set(linhas[1].split())

        # 3a linha: estados finais -> Estado:reconhece
        for par in linhas[2].split():
            estado, token = par.split(":")
            self.estados_finais[estado] = token

        # 4a linha em diante: regras de transicao -> EstadoInicial:simbolo:EstadoFinal
        for linha in linhas[3:]:
            for regra in linha.split():
                origem, simbolo, destino = regra.split(":")
                self.transicoes[(origem, simbolo)] = destino

    def reconhece_termo(self, termo: str):
        """Simula o AFD para um termo. Retorna o nome do token reconhecido
        ou None se o termo nao for aceito pelo automato."""
        estado_atual = self.estado_inicial

        for caractere in termo:
            if caractere not in self.simbolos:
                return None

            proximo_estado = self.transicoes.get((estado_atual, caractere))
            if proximo_estado is None:
                return None  # nao ha transicao definida: termo rejeitado

            estado_atual = proximo_estado

        return self.estados_finais.get(estado_atual)  # None se nao for estado final


def extrair_tokens(caminho_entrada: Path):
    """Le o arquivo de entrada e retorna uma lista de (token, linha, coluna).
    Os termos sao separados por espaco em branco; suporta mais de um token
    por linha."""
    tokens = []
    with open(caminho_entrada, encoding="utf-8") as arquivo:
        for num_linha, linha in enumerate(arquivo, start=1):
            coluna = 1
            for pedaco in linha.split(" "):
                termo = pedaco.strip("\n\r\t")
                inicio_coluna = coluna
                coluna += len(pedaco)
                if termo:
                    tokens.append((termo, num_linha, inicio_coluna))
    return tokens


def montar_tabela_simbolos(afd: AFD, tokens):
    tabela = []
    for idx, (termo, linha, coluna) in enumerate(tokens, start=1):
        tipo = afd.reconhece_termo(termo)
        tabela.append({
            "ID": idx,
            "TOKEN": termo,
            "TIPO": tipo if tipo else "NAO_RECONHECIDO",
            "LINHA": linha,
            "COLUNA": coluna,
        })
    return tabela


def exportar_csv(tabela, caminho_saida: Path):
    with open(caminho_saida, "w", newline="", encoding="utf-8") as arquivo:
        campos = ["ID", "TOKEN", "TIPO", "LINHA", "COLUNA"]
        escritor = csv.DictWriter(arquivo, fieldnames=campos, delimiter=";")
        escritor.writeheader()
        escritor.writerows(tabela)


def main():
    pasta = Path(__file__).parent
    caminho_config = Path(sys.argv[1]) if len(sys.argv) > 1 else pasta / "configAfd.md"
    caminho_entrada = Path(sys.argv[2]) if len(sys.argv) > 2 else pasta / "entrada.txt"
    caminho_saida = pasta / "tabela_simbolos.csv"

    afd = AFD(caminho_config)
    tokens = extrair_tokens(caminho_entrada)
    tabela = montar_tabela_simbolos(afd, tokens)

    print(f"{'ID':<4}{'TOKEN':<15}{'TIPO':<18}{'LINHA':<7}{'COLUNA':<7}")
    for item in tabela:
        print(f"{item['ID']:<4}{item['TOKEN']:<15}{item['TIPO']:<18}{item['LINHA']:<7}{item['COLUNA']:<7}")

    exportar_csv(tabela, caminho_saida)
    print(f"\nTabela de simbolos exportada para: {caminho_saida}")


if __name__ == "__main__":
    main()
