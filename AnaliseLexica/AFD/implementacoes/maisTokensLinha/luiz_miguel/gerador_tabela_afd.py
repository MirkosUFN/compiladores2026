import os
import sys
import json


class Simbolo(dict):
    """
    Representa uma entrada na Tabela de Símbolos.
    Permite acesso a campos tanto em minúsculas quanto maiúsculas
    (ex: item['token'] ou item['TOKEN'], item['coluna'] ou item['COLUNA']).
    """
    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        key_str = str(key).lower()
        for k in self:
            if k.lower() == key_str:
                return super().__getitem__(k)
        return super().__getitem__(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default


def carregar_afd(caminho_config):
    """
    Carrega as configurações do AFD a partir do arquivo de configuração.
    Formato esperado:
    - Linha 1: Estados separados por espaço (o primeiro é o inicial)
    - Linha 2: Símbolos do alfabeto separados por espaço
    - Linha 3: Estados finais e seus tokens no formato Estado:TOKEN separados por espaço
    - Linhas 4+: Regras de transição no formato EstadoOrigem:Simbolo:EstadoDestino
    """
    with open(caminho_config, 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]

    if len(linhas) < 3:
        raise ValueError("Arquivo de configuração do AFD inválido ou incompleto.")

    estados = linhas[0].split()
    estado_inicial = estados[0]
    simbolos = set(linhas[1].split())

    estados_finais = {}
    for ef in linhas[2].split():
        if ':' in ef:
            est, token = ef.split(':', 1)
            estados_finais[est] = token

    transicoes = {}
    for linha_regras in linhas[3:]:
        for regra in linha_regras.split():
            partes = regra.split(':')
            if len(partes) == 3:
                origem, sim, destino = partes
                transicoes[(origem, sim)] = destino

    return estado_inicial, simbolos, estados_finais, transicoes


def extrair_proximo_token(linha, inicio, estado_inicial, simbolos, estados_finais, transicoes):
    """
    Extrai o maior token válido a partir da posição 'inicio' usando o AFD.
    Retorna ((token, tipo, coluna), proxima_posicao) ou (None, proxima_posicao).
    A coluna é calculada de forma 1-indexada onde o token se inicia na linha.
    """
    i = inicio
    while i < len(linha) and linha[i].isspace():
        i += 1

    if i >= len(linha):
        return None, i

    estado_atual = estado_inicial
    ultimo_token_valido = None
    ultimo_tipo_valido = None
    posicao_fim_valida = i

    for j in range(i, len(linha)):
        caractere = linha[j]

        if caractere not in simbolos:
            break

        chave = (estado_atual, caractere)
        if chave in transicoes:
            estado_atual = transicoes[chave]
            if estado_atual in estados_finais:
                ultimo_token_valido = linha[i:j+1]
                ultimo_tipo_valido = estados_finais[estado_atual]
                posicao_fim_valida = j + 1
        else:
            break

    coluna = i + 1  # 1-indexada

    if ultimo_token_valido is None:
        termo_erro = linha[i]
        return (termo_erro, "ERRO_LEXICO", coluna), i + 1

    return (ultimo_token_valido, ultimo_tipo_valido, coluna), posicao_fim_valida


def processar_codigo_fonte(caminho_fonte, estado_inicial, simbolos, estados_finais, transicoes):
    """
    Lê o arquivo de código-fonte e gera a Tabela de Símbolos.
    Cada entrada contém as colunas: ID, token, tipo, linha e coluna.
    """
    tabela_simbolos = []
    id_counter = 1

    with open(caminho_fonte, 'r', encoding='utf-8') as f:
        for num_linha, linha in enumerate(f, start=1):
            posicao = 0
            tamanho = len(linha)

            while posicao < tamanho:
                resultado, proxima_pos = extrair_proximo_token(
                    linha, posicao, estado_inicial, simbolos, estados_finais, transicoes
                )

                if resultado is None:
                    break

                termo, tipo, coluna = resultado

                tabela_simbolos.append(Simbolo({
                    "ID": id_counter,
                    "token": termo,
                    "tipo": tipo,
                    "linha": num_linha,
                    "coluna": coluna
                }))
                id_counter += 1
                posicao = proxima_pos

    return tabela_simbolos


def imprimir_tabela(tabela):
    """
    Exibe a Tabela de Símbolos formatada no terminal.
    """
    if not tabela:
        print("\n[!] Tabela de símbolos vazia.")
        return

    colunas = ["ID", "token", "tipo", "linha", "coluna"]
    larguras = {col: len(col) for col in colunas}
    for item in tabela:
        for col in colunas:
            val = str(item.get(col, ""))
            if len(val) > larguras[col]:
                larguras[col] = len(val)

    separador = "+" + "+".join("-" * (larguras[col] + 2) for col in colunas) + "+"
    cabecalho = "|" + "|".join(f" {col:<{larguras[col]}} " for col in colunas) + "|"

    print("\n" + separador)
    print(cabecalho)
    print(separador)
    for item in tabela:
        linha_str = "|" + "|".join(f" {str(item.get(col, '')):<{larguras[col]}} " for col in colunas) + "|"
        print(linha_str)
    print(separador + "\n")


def salvar_tabela_json(tabela, caminho_saida):
    """
    Salva a Tabela de Símbolos no formato JSON.
    """
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(tabela, f, ensure_ascii=False, indent=4)
    print(f"[+] Tabela de símbolos salva com sucesso em: {caminho_saida}")


def resolver_caminhos():
    """
    Resolve caminhos para configuração, código-fonte e JSON de saída.
    Permite passar arquivos pela linha de comando:
    python gerador_tabela_afd.py [caminho_fonte] [caminho_config] [caminho_json]
    """
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))

    # 1. Configuração do AFD (configAfd.md por padrão)
    caminho_config = None
    if len(sys.argv) > 2:
        caminho_config = sys.argv[2]
    else:
        for nome in ['configAfd.md', 'AFD_config.txt']:
            candidato_local = os.path.join(diretorio_atual, nome)
            if os.path.exists(candidato_local):
                caminho_config = candidato_local
                break
            if os.path.exists(nome):
                caminho_config = os.path.abspath(nome)
                break
        if not caminho_config:
            caminho_config = os.path.join(diretorio_atual, 'configAfd.md')

    # 2. Arquivo-fonte (input.c ou codigo.txt)
    caminho_fonte = None
    if len(sys.argv) > 1:
        caminho_fonte = sys.argv[1]
    else:
        for nome in ['input.c', 'codigo.txt']:
            candidato_local = os.path.join(diretorio_atual, nome)
            if os.path.exists(candidato_local):
                caminho_fonte = candidato_local
                break
            if os.path.exists(nome):
                caminho_fonte = os.path.abspath(nome)
                break
        if not caminho_fonte:
            caminho_fonte = os.path.join(diretorio_atual, 'input.c')

    # 3. JSON de saída
    if len(sys.argv) > 3:
        caminho_json = sys.argv[3]
    else:
        caminho_json = os.path.join(diretorio_atual, 'TabSimbolos.json')

    return caminho_config, caminho_fonte, caminho_json


def main():
    caminho_config, caminho_fonte, caminho_json = resolver_caminhos()

    if not os.path.exists(caminho_config):
        print(f"Erro: Arquivo de configuração '{caminho_config}' não encontrado.")
        return

    print(f"[*] Carregando configuração do AFD: {os.path.basename(caminho_config)}")
    estado_inicial, simbolos, estados_finais, transicoes = carregar_afd(caminho_config)

    if os.path.exists(caminho_fonte):
        print(f"[*] Processando código-fonte: {os.path.basename(caminho_fonte)}")
        tabela = processar_codigo_fonte(caminho_fonte, estado_inicial, simbolos, estados_finais, transicoes)
        imprimir_tabela(tabela)
        salvar_tabela_json(tabela, caminho_json)
    else:
        print(f"Erro: Arquivo-fonte '{caminho_fonte}' não encontrado. Crie o arquivo para testar.")


if __name__ == '__main__':
    main()