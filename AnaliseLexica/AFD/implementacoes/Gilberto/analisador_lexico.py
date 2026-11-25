import csv
import os
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

@dataclass
class AFD:
    """Autômato Finito Determinístico montado a partir do arquivo de configuração."""
    estados: List[str]
    simbolos: Set[str]
    finais: Dict[str, str]
    transicoes: Dict[Tuple[str, str], str] = field(default_factory=dict)

    @property
    def inicial(self) -> str:
        return self.estados[0]

    def reconhecer(self, palavra: str) -> Tuple[bool, Optional[str], str]:
        """
        Simula o AFD sobre a palavra inteira.
        Retorna (aceita, token_reconhecido, mensagem).
        """
        estado = self.inicial
        for posicao, simbolo in enumerate(palavra, start=1):
            if simbolo not in self.simbolos:
                return False, None, f"símbolo '{simbolo}' (posição {posicao}) não pertence ao alfabeto"
            proximo = self.transicoes.get((estado, simbolo))
            if proximo is None:
                return False, None, f"sem transição de {estado} com '{simbolo}' (posição {posicao})"
            estado = proximo

        if estado in self.finais:
            return True, self.finais[estado], f"terminou no estado final {estado}"
        return False, None, f"terminou no estado {estado}, que não é final"


def carregar_afd(caminho: str) -> AFD:
    """Lê o configAfd.md e monta o AFD."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    if len(linhas) < 4:
        raise ValueError("configAfd.md precisa de pelo menos 4 linhas (estados, símbolos, finais e transições).")

    estados = linhas[0].split()
    simbolos = set(linhas[1].split())

    finais: Dict[str, str] = {}
    for item in linhas[2].split():
        estado, token = item.split(":", 1)
        if estado not in estados:
            raise ValueError(f"Estado final '{estado}' não está na lista de estados.")
        finais[estado] = token

    afd = AFD(estados=estados, simbolos=simbolos, finais=finais)

    for numero, linha in enumerate(linhas[3:], start=4):
        for regra in linha.split():
            # split pela esquerda e pela direita permite que o símbolo seja ':'
            origem, resto = regra.split(":", 1)
            simbolo, destino = resto.rsplit(":", 1)
            if origem not in estados or destino not in estados:
                raise ValueError(f"Linha {numero}: regra '{regra}' usa estado inexistente.")
            if simbolo not in simbolos:
                raise ValueError(f"Linha {numero}: regra '{regra}' usa símbolo fora do alfabeto.")
            if (origem, simbolo) in afd.transicoes:
                raise ValueError(f"Linha {numero}: regra '{regra}' torna o autômato não determinístico.")
            afd.transicoes[(origem, simbolo)] = destino

    return afd


def processar_arquivo(afd: AFD, caminho_entrada: str, caminho_csv: str) -> None:
    """Analisa cada linha do arquivo de entrada (um termo por linha) e gera a tabela de símbolos."""
    with open(caminho_entrada, "r", encoding="utf-8") as entrada, \
         open(caminho_csv, "w", newline="", encoding="utf-8-sig") as saida:
        tabela = csv.writer(saida, delimiter=";", lineterminator="\n")
        tabela.writerow(["ID", "Token", "Tipo", "Linha"])

        proximo_id = 1
        aceitos = rejeitados = 0

        for numero_linha, linha in enumerate(entrada, start=1):
            termo = linha.strip()
            if not termo:
                continue

            aceita, tipo, mensagem = afd.reconhecer(termo)
            if aceita:
                tabela.writerow([proximo_id, termo, tipo, numero_linha])
                print(f"  Linha {numero_linha:>3}: {termo!r:<15} -> ACEITO   ({tipo})")
                proximo_id += 1
                aceitos += 1
            else:
                print(f"  Linha {numero_linha:>3}: {termo!r:<15} -> REJEITADO ({mensagem})")
                rejeitados += 1

    print(f"\nTotal: {aceitos} aceito(s), {rejeitados} rejeitado(s).")


def main() -> None:
    diretorio = os.path.dirname(os.path.abspath(__file__))
    caminho_config = os.path.join(diretorio, "configAfd.md")
    caminho_entrada = sys.argv[1] if len(sys.argv) > 1 else os.path.join(diretorio, "entrada.txt")
    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")

    afd = carregar_afd(caminho_config)
    print(f"AFD carregado: {len(afd.estados)} estados, {len(afd.simbolos)} símbolos, "
          f"{len(afd.transicoes)} transições. Estado inicial: {afd.inicial}\n")

    processar_arquivo(afd, caminho_entrada, caminho_csv)
    print(f"Tabela de símbolos salva em: {caminho_csv}")


if __name__ == "__main__":
    main()
