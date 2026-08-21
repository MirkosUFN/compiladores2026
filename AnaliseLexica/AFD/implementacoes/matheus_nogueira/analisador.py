import csv
import os
import re
from dataclasses import dataclass
from typing import Dict, Optional, Set, Tuple


PALAVRAS_RESERVADAS_C = {
    "auto", "break", "case", "char", "const", "continue", "default", "do",
    "double", "else", "enum", "extern", "float", "for", "goto", "if",
    "inline", "int", "long", "register", "restrict", "return", "short",
    "signed", "sizeof", "static", "struct", "switch", "typedef", "union",
    "unsigned", "void", "volatile", "while",
    "_Alignas", "_Alignof", "_Atomic", "_Bool", "_Complex", "_Generic",
    "_Imaginary", "_Noreturn", "_Static_assert", "_Thread_local",
    "alignas", "alignof", "bool", "constexpr", "false", "nullptr",
    "static_assert", "thread_local", "true", "typeof", "typeof_unqual",
    "_BitInt", "_Decimal32", "_Decimal64", "_Decimal128",
}

ESTADO_ERRO = "QE"


@dataclass
class AFD:
    """Representa a definição de um autômato finito determinístico."""

    estado_inicial: str
    simbolos: Set[str]
    estados_finais: Dict[str, str]
    transicoes: Dict[Tuple[str, str], str]


@dataclass
class ResultadoAnalise:
    """Representa o resultado da análise léxica de um lexema."""

    lexema: str
    aceito: bool
    token: str
    tipo: str
    estado_final: str
    mensagem: str


def carregar_afd(caminho_config: str) -> AFD:
    """
    Carrega a definição do AFD a partir de um arquivo de configuração.

    O arquivo deve conter os estados na primeira linha, o alfabeto na segunda,
    os estados finais na terceira e as transições nas linhas seguintes.
    """
    with open(caminho_config, "r", encoding="utf-8") as arquivo:
        linhas = [
            linha.strip()
            for linha in arquivo.readlines()
            if linha.strip() and not linha.lstrip().startswith("#")
        ]

    if len(linhas) < 4:
        raise ValueError("Arquivo configAfd.md inválido ou incompleto.")

    estados = linhas[0].split()
    estado_inicial = estados[0]
    simbolos = set(linhas[1].split())

    estados_finais: Dict[str, str] = {}

    for item in linhas[2].split():
        estado, classificacao = item.split(":", 1)
        estados_finais[estado] = classificacao

    transicoes: Dict[Tuple[str, str], str] = {}

    for linha in linhas[3:]:
        for regra in linha.split():
            origem, simbolo, destino = regra.split(":", 2)
            transicoes[(origem, simbolo)] = destino

    estados_definidos = set(estados)

    if ESTADO_ERRO not in estados_definidos:
        raise ValueError(
            f"O estado de erro '{ESTADO_ERRO}' precisa estar declarado no configAfd.md."
        )

    for estado_final in estados_finais:
        if estado_final not in estados_definidos:
            raise ValueError(f"Estado final '{estado_final}' não foi declarado.")

    for (origem, simbolo), destino in transicoes.items():
        if origem not in estados_definidos:
            raise ValueError(f"Estado de origem '{origem}' não foi declarado.")

        if destino not in estados_definidos:
            raise ValueError(f"Estado de destino '{destino}' não foi declarado.")

        if simbolo not in simbolos:
            raise ValueError(
                f"Símbolo '{simbolo}' usado em uma transição não pertence ao alfabeto."
            )

    return AFD(
        estado_inicial=estado_inicial,
        simbolos=simbolos,
        estados_finais=estados_finais,
        transicoes=transicoes,
    )


def executar_afd(
    lexema: str,
    afd: AFD,
    mostrar_transicoes: bool = False,
):
    """
    Executa o AFD caractere por caractere.

    Transições inexistentes levam ao estado morto QE. Após alcançar QE,
    o autômato permanece nesse estado até o final da entrada.
    """
    estado_atual = afd.estado_inicial
    motivo_erro: Optional[str] = None

    if mostrar_transicoes:
        print(f"\n  Estado inicial: {estado_atual}")

    for caractere in lexema:
        if estado_atual == ESTADO_ERRO:
            if mostrar_transicoes:
                print(f"  {ESTADO_ERRO} --{caractere}--> {ESTADO_ERRO}")
            continue

        if caractere not in afd.simbolos:
            motivo_erro = f"Símbolo '{caractere}' não pertence ao alfabeto."

            if mostrar_transicoes:
                print(
                    f"  {estado_atual} --{caractere}--> "
                    f"{ESTADO_ERRO}  [ERRO]"
                )

            estado_atual = ESTADO_ERRO
            continue

        chave = (estado_atual, caractere)

        if chave in afd.transicoes:
            proximo_estado = afd.transicoes[chave]
        else:
            proximo_estado = ESTADO_ERRO

            if motivo_erro is None:
                motivo_erro = (
                    f"Não existe transição válida a partir de "
                    f"'{estado_atual}' com o símbolo '{caractere}'."
                )

        if mostrar_transicoes:
            sufixo = "  [ERRO]" if proximo_estado == ESTADO_ERRO else ""
            print(f"  {estado_atual} --{caractere}--> {proximo_estado}{sufixo}")

        estado_atual = proximo_estado

    if estado_atual == ESTADO_ERRO:
        return False, estado_atual, None, motivo_erro

    classificacao = afd.estados_finais.get(estado_atual)

    if classificacao is None:
        return (
            False,
            estado_atual,
            None,
            f"O termo terminou no estado não-final '{estado_atual}'.",
        )

    return True, estado_atual, classificacao, None


def parece_identificador_invalido(lexema: str) -> bool:
    """
    Identifica lexemas que se assemelham a identificadores,
    mas começam por número ou sinal.
    """
    return bool(
        re.fullmatch(r"[+-]?\d+[A-Za-z_][A-Za-z0-9_]*", lexema)
        or re.fullmatch(r"[+-][A-Za-z_][A-Za-z0-9_]*", lexema)
    )


def validar_identificador_c(lexema: str):
    """
    Valida um identificador conforme as regras léxicas utilizadas para C.

    O identificador deve começar por letra ou sublinhado, pode conter letras,
    números e sublinhados nas posições seguintes e não pode ser uma palavra
    reservada da linguagem C.

    A comparação de palavras reservadas é sensível a maiúsculas e minúsculas.
    """
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", lexema):
        return False, "Nome de variável inválido em C."

    if lexema in PALAVRAS_RESERVADAS_C:
        return False, f"'{lexema}' é uma palavra reservada da linguagem C."

    return True, "Nome de variável válido."


def analisar_lexema(
    lexema: str,
    afd: AFD,
    mostrar_transicoes: bool = False,
) -> ResultadoAnalise:
    """
    Executa a análise léxica completa de um lexema.

    O AFD reconhece a estrutura do termo e, quando o resultado for um
    identificador, uma validação adicional verifica as palavras reservadas de C.
    """
    lexema = lexema.strip()

    if not lexema:
        return ResultadoAnalise(
            lexema="",
            aceito=False,
            token="ERRO",
            tipo="VAZIO",
            estado_final=afd.estado_inicial,
            mensagem="Termo vazio.",
        )

    aceito, estado_final, classificacao, erro = executar_afd(
        lexema,
        afd,
        mostrar_transicoes=mostrar_transicoes,
    )

    if not aceito and parece_identificador_invalido(lexema):
        return ResultadoAnalise(
            lexema=lexema,
            aceito=False,
            token="ERRO",
            tipo="NOME_VARIAVEL_INVALIDO",
            estado_final=estado_final,
            mensagem=(
                f"'{lexema}' parece um nome de variável, mas é inválido "
                "porque um identificador em C não pode começar com número "
                "ou sinal."
            ),
        )

    if not aceito:
        return ResultadoAnalise(
            lexema=lexema,
            aceito=False,
            token="ERRO",
            tipo="NAO_RECONHECIDO",
            estado_final=estado_final,
            mensagem=erro or "Termo não reconhecido.",
        )

    if classificacao == "INTEIRO":
        return ResultadoAnalise(
            lexema=lexema,
            aceito=True,
            token="NUMERO",
            tipo="INTEIRO",
            estado_final=estado_final,
            mensagem="Número inteiro reconhecido.",
        )

    if classificacao == "FRACIONARIO":
        return ResultadoAnalise(
            lexema=lexema,
            aceito=True,
            token="NUMERO",
            tipo="FRACIONARIO",
            estado_final=estado_final,
            mensagem="Número fracionário reconhecido.",
        )

    if classificacao == "NOMEVARIAVEL":
        valido, mensagem = validar_identificador_c(lexema)

        if not valido:
            return ResultadoAnalise(
                lexema=lexema,
                aceito=False,
                token="ERRO",
                tipo="NOME_VARIAVEL_INVALIDO",
                estado_final=estado_final,
                mensagem=mensagem,
            )

        return ResultadoAnalise(
            lexema=lexema,
            aceito=True,
            token="IDENTIFICADOR",
            tipo="NOME_VARIAVEL",
            estado_final=estado_final,
            mensagem=mensagem,
        )

    return ResultadoAnalise(
        lexema=lexema,
        aceito=True,
        token="DESCONHECIDO",
        tipo=classificacao,
        estado_final=estado_final,
        mensagem="Termo reconhecido.",
    )


def criar_tabela_simbolos(caminho_csv: str):
    """
    Cria a tabela de símbolos com as colunas ID, LEXEMA, TOKEN, TIPO e LINHA.
    """
    with open(
        caminho_csv,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow(["ID", "LEXEMA", "TOKEN", "TIPO", "LINHA"])


def adicionar_tabela_simbolos(
    caminho_csv: str,
    id_registro: int,
    resultado: ResultadoAnalise,
    linha: int,
):
    """
    Adiciona um lexema aceito à tabela de símbolos.
    """
    with open(
        caminho_csv,
        "a",
        newline="",
        encoding="utf-8-sig",
    ) as arquivo:
        escritor = csv.writer(arquivo, delimiter=";")
        escritor.writerow([
            id_registro,
            resultado.lexema,
            resultado.token,
            resultado.tipo,
            linha,
        ])


def mostrar_resultado(resultado: ResultadoAnalise):
    """
    Exibe no terminal o resultado da análise de um lexema.
    """
    status = "ACEITO" if resultado.aceito else "REJEITADO"

    print(f"\n[{status}] {resultado.lexema}")
    print(f"  Token        : {resultado.token}")
    print(f"  Tipo         : {resultado.tipo}")
    print(f"  Estado final : {resultado.estado_final}")
    print(f"  Mensagem     : {resultado.mensagem}")


def processar_arquivo(
    caminho_entrada: str,
    caminho_csv: str,
    afd: AFD,
    proximo_id: int,
) -> int:
    """
    Processa um lexema por linha e registra os termos aceitos na tabela de símbolos.
    """
    with open(caminho_entrada, "r", encoding="utf-8") as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            lexema = linha.strip()

            if not lexema:
                continue

            resultado = analisar_lexema(lexema, afd)
            mostrar_resultado(resultado)

            if resultado.aceito:
                adicionar_tabela_simbolos(
                    caminho_csv,
                    proximo_id,
                    resultado,
                    numero_linha,
                )
                proximo_id += 1

    return proximo_id


def main():
    """Inicializa o analisador léxico em modo de arquivo e modo interativo."""
    diretorio = os.path.dirname(os.path.abspath(__file__))

    caminho_config = os.path.join(diretorio, "configAfd.md")
    caminho_entrada = os.path.join(diretorio, "entrada.txt")
    caminho_csv = os.path.join(diretorio, "tabela_simbolos.csv")

    afd = carregar_afd(caminho_config)

    criar_tabela_simbolos(caminho_csv)

    proximo_id = 1

    print("=" * 67)
    print(" ANALISADOR LÉXICO - AFD + IDENTIFICADORES DA LINGUAGEM C")
    print("=" * 67)

    if os.path.exists(caminho_entrada):
        print("\nProcessando entrada.txt...")

        proximo_id = processar_arquivo(
            caminho_entrada,
            caminho_csv,
            afd,
            proximo_id,
        )

    print("\n" + "=" * 67)
    print("MODO INTERATIVO")
    print("Digite um termo por vez.")
    print("")
    print("Comandos:")
    print("  sair")
    print("  transicoes TERMO")
    print("=" * 67)

    linha_interativa = 1

    while True:
        try:
            entrada = input("\nDigite o termo: ").strip()

            if entrada.lower() in {"sair", "exit"}:
                break

            if not entrada:
                continue

            mostrar_transicoes = False
            lexema = entrada

            if entrada.lower().startswith("transicoes "):
                lexema = entrada[len("transicoes "):].strip()
                mostrar_transicoes = True

            resultado = analisar_lexema(
                lexema,
                afd,
                mostrar_transicoes=mostrar_transicoes,
            )

            mostrar_resultado(resultado)

            if resultado.aceito:
                adicionar_tabela_simbolos(
                    caminho_csv,
                    proximo_id,
                    resultado,
                    linha_interativa,
                )
                proximo_id += 1

            linha_interativa += 1

        except (KeyboardInterrupt, EOFError):
            print()
            break

    print(f"\nTabela de símbolos salva em:\n{caminho_csv}")
    print("\nAnalisador encerrado.")


if __name__ == "__main__":
    main()
