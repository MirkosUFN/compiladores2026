from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class NoArvore:
    """Nó da árvore de derivação.

    ``simbolo`` representa um não terminal ou terminal da gramática.
    ``lexema`` guarda o trecho concreto correspondente ao terminal.
    """

    simbolo: str
    lexema: Optional[str] = None
    filhos: List["NoArvore"] = field(default_factory=list)

    def rotulo(self) -> str:
        if self.lexema is None:
            return self.simbolo
        return f"{self.simbolo} [{self.lexema}]"


def terminal(simbolo: str, lexema: str) -> NoArvore:
    """Cria um terminal da árvore com seu lexema concreto."""
    return NoArvore(simbolo=simbolo, lexema=lexema)


def condicao(nome: str, operador: str, valor: str) -> NoArvore:
    """Monta CONDICAO -> NOMEVAR COMPARACAO VALOR."""
    return NoArvore(
        "CONDICAO",
        filhos=[
            terminal("NOMEVAR", nome),
            NoArvore(
                "COMPARACAO",
                filhos=[terminal(operador, operador)],
            ),
            NoArvore(
                "VALOR",
                filhos=[terminal("INTEIRO", valor)],
            ),
        ],
    )


def sif(nome: str, operador: str, valor: str, bloco: NoArvore) -> NoArvore:
    """Monta SIF -> PR:IF AP CONDICAO FP ACH BLOCO FCH."""
    return NoArvore(
        "SIF",
        filhos=[
            terminal("PR:IF", "if"),
            terminal("AP", "("),
            condicao(nome, operador, valor),
            terminal("FP", ")"),
            terminal("ACH", "{"),
            bloco,
            terminal("FCH", "}"),
        ],
    )


def construir_arvore() -> NoArvore:
    """Constrói a árvore da sentença presente no README do exercício.

    A gramática simplificada usa ``BLOCO -> ...`` para representar comandos
    que não foram detalhados. Por isso, ``w=10;`` aparece como o lexema
    concreto do terminal ``...`` no bloco mais interno.
    """
    bloco_interno = NoArvore(
        "BLOCO",
        filhos=[terminal("...", "w=10;")],
    )

    sif_interno = sif("y", ">", "0", bloco_interno)
    bloco_externo = NoArvore("BLOCO", filhos=[sif_interno])

    return sif("x", ">", "0", bloco_externo)


def renderizar_ascii(raiz: NoArvore) -> str:
    """Renderiza a árvore em formato de texto usando ramificações ASCII."""
    linhas = [raiz.rotulo()]

    def visitar(no: NoArvore, prefixo: str, eh_ultimo: bool) -> None:
        galho = "└── " if eh_ultimo else "├── "
        linhas.append(prefixo + galho + no.rotulo())

        novo_prefixo = prefixo + ("    " if eh_ultimo else "│   ")
        for indice, filho in enumerate(no.filhos):
            visitar(filho, novo_prefixo, indice == len(no.filhos) - 1)

    for indice, filho in enumerate(raiz.filhos):
        visitar(filho, "", indice == len(raiz.filhos) - 1)

    return "\n".join(linhas)


def renderizar_dot(raiz: NoArvore) -> str:
    """Renderiza a árvore no formato DOT, compatível com Graphviz."""
    linhas = ["digraph ArvoreDerivacao {", "    rankdir=TB;", "    node [shape=box];"]
    contador = 0

    def escapar(texto: str) -> str:
        return texto.replace("\\", "\\\\").replace('"', '\\"')

    def visitar(no: NoArvore, pai: Optional[int] = None) -> None:
        nonlocal contador
        identificador = contador
        contador += 1
        rotulo = escapar(no.rotulo())
        linhas.append(f'    n{identificador} [label="{rotulo}"];')

        if pai is not None:
            linhas.append(f"    n{pai} -> n{identificador};")

        for filho in no.filhos:
            visitar(filho, identificador)

    visitar(raiz)
    linhas.append("}")
    return "\n".join(linhas)


def main() -> None:
    diretorio = Path(__file__).resolve().parent
    arvore = construir_arvore()
    arvore_ascii = renderizar_ascii(arvore)
    arvore_dot = renderizar_dot(arvore)

    caminho_ascii = diretorio / "arvore_derivacao.txt"
    caminho_dot = diretorio / "arvore_derivacao.dot"

    caminho_ascii.write_text(arvore_ascii + "\n", encoding="utf-8")
    caminho_dot.write_text(arvore_dot + "\n", encoding="utf-8")

    print(arvore_ascii)
    print(f"\nÁrvore ASCII salva em: {caminho_ascii}")
    print(f"Árvore DOT salva em: {caminho_dot}")


if __name__ == "__main__":
    main()
