import csv
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


# Gilberto Morales

@dataclass
class AFD:
    estados: List[str]
    simbolos: Set[str]
    finais: Dict[str, str]
    transicoes: Dict[Tuple[str, str], str] = field(default_factory=dict)

    @property
    def inicial(self) -> str:
        return self.estados[0]

    def maior_prefixo(self, texto: str, inicio: int) -> Tuple[int, Optional[str]]:
        """
        Percorre o AFD a partir de texto[inicio] enquanto houver transição e
        guarda o último ponto em que esteve em um estado final.
        Retorna (posição_final_exclusiva, token). Se nada foi aceito, token = None.
        """
        estado = self.inicial
        ultimo_fim, ultimo_token = inicio, None
        posicao = inicio
        while posicao < len(texto):
            proximo = self.transicoes.get((estado, texto[posicao]))
            if proximo is None:
                break
            estado = proximo
            posicao += 1
            if estado in self.finais:
                ultimo_fim, ultimo_token = posicao, self.finais[estado]
        return ultimo_fim, ultimo_token


@dataclass
class Token:
    lexema: str
    tipo: str
    linha: int
    coluna: int


@dataclass
class ErroLexico:
    lexema: str
    linha: int
    coluna: int


def carregar_afd(caminho: str) -> AFD:
    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    if len(linhas) < 4:
        raise ValueError("AFD_config.txt precisa de pelo menos 4 linhas.")

    estados = linhas[0].split()
    simbolos = set(linhas[1].split())
    finais = {}
    for item in linhas[2].split():
        estado, token = item.split(":", 1)
        finais[estado] = token

    afd = AFD(estados=estados, simbolos=simbolos, finais=finais)
    for numero, linha in enumerate(linhas[3:], start=4):
        for regra in linha.split():
            origem, resto = regra.split(":", 1)
            simbolo, destino = resto.rsplit(":", 1)
            if origem not in estados or destino not in estados:
                raise ValueError(f"Linha {numero}: regra '{regra}' usa estado inexistente.")
            if simbolo not in simbolos:
                raise ValueError(f"Linha {numero}: regra '{regra}' usa símbolo fora do alfabeto.")
            afd.transicoes[(origem, simbolo)] = destino
    return afd


def analisar_linha(afd: AFD, texto: str, numero_linha: int) -> Tuple[List[Token], List[ErroLexico]]:
    """Quebra a linha em tokens, registrando linha e coluna (contadas a partir de 1)."""
    tokens: List[Token] = []
    erros: List[ErroLexico] = []
    posicao = 0

    while posicao < len(texto):
        if texto[posicao].isspace():
            posicao += 1
            continue

        fim, tipo = afd.maior_prefixo(texto, posicao)
        if tipo is not None:
            tokens.append(Token(texto[posicao:fim], tipo, numero_linha, posicao + 1))
            posicao = fim
        else:
            # Nenhum token reconhecido: descarta o trecho até o próximo espaço
            fim = posicao
            while fim < len(texto) and not texto[fim].isspace():
                fim += 1
            erros.append(ErroLexico(texto[posicao:fim], numero_linha, posicao + 1))
            posicao = fim

    return tokens, erros


def processar_arquivo(afd: AFD, caminho_entrada: str, caminho_csv: str) -> None:
    todos_tokens: List[Token] = []
    todos_erros: List[ErroLexico] = []

    with open(caminho_entrada, "r", encoding="utf-8") as entrada:
        for numero_linha, linha in enumerate(entrada, start=1):
            texto = linha.rstrip("\n").expandtabs(4)
            tokens, erros = analisar_linha(afd, texto, numero_linha)
            todos_tokens.extend(tokens)
            todos_erros.extend(erros)

    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as saida:
        tabela = csv.writer(saida, delimiter=";", lineterminator="\n")
        tabela.writerow(["ID", "Token", "Tipo", "Linha", "Coluna"])
        for identificador, token in enumerate(todos_tokens, start=1):
            tabela.writerow([identificador, token.lexema, token.tipo, token.linha, token.coluna])

    print(f"{'ID':>3}  {'Token':<12} {'Tipo':<18} {'Linha':>5} {'Coluna':>6}")
    print("-" * 48)
    for identificador, token in enumerate(todos_tokens, start=1):
        print(f"{identificador:>3}  {token.lexema:<12} {token.tipo:<18} {token.linha:>5} {token.coluna:>6}")

    if todos_erros:
        print("\nErros léxicos:")
        for erro in todos_erros:
            print(f"  Linha {erro.linha}, coluna {erro.coluna}: '{erro.lexema}' não é reconhecido pelo AFD")

    print(f"\n{len(todos_tokens)} token(s) reconhecido(s), {len(todos_erros)} erro(s).")


def main() -> None:
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_config = os.path.join(diretorio, "AFD_config.txt")
    caminho_entrada = sys.argv[1] if len(sys.argv) > 1 else os.path.join(diretorio, "input.c")
    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")

    afd = carregar_afd(caminho_config)
    processar_arquivo(afd, caminho_entrada, caminho_csv)
    print(f"Tabela de símbolos salva em: {caminho_csv}")


if __name__ == "__main__":
    main()
