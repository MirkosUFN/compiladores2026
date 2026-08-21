import os
import json

def carregar_afd(caminho_config):
    """
    Carrega as configurações do AFD a partir do arquivo de configuração.
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


def reconhecer_termo(termo, estado_inicial, simbolos, estados_finais, transicoes):
    """
    Processa um termo pelo AFD e retorna o TIPO (categoria) se for válido.
    """
    estado_atual = estado_inicial

    for caractere in termo:
        if caractere not in simbolos:
            return None
        
        chave = (estado_atual, caractere)
        if chave in transicoes:
            estado_atual = transicoes[chave]
        else:
            return None

    if estado_atual in estados_finais:
        return estados_finais[estado_atual]
    return None


def processar_codigo_fonte(caminho_fonte, estado_inicial, simbolos, estados_finais, transicoes):
    """
    Lê o arquivo de código-fonte linha por linha e constrói a Tabela de Símbolos.
    """
    tabela_simbolos = []
    id_counter = 1

    with open(caminho_fonte, 'r', encoding='utf-8') as f:
        for num_linha, linha in enumerate(f, start=1):
            termos = linha.strip().split()
            for termo in termos:
                tipo = reconhecer_termo(termo, estado_inicial, simbolos, estados_finais, transicoes)
                
                tabela_simbolos.append({
                    "ID": id_counter,
                    "TOKEN": termo,
                    "TIPO": tipo if tipo else "ERRO_LEXICO",
                    "LINHA": num_linha
                })
                id_counter += 1

    return tabela_simbolos


def salvar_tabela_json(tabela, caminho_saida):
    """
    Salva a Tabela de Símbolos no formato JSON.
    """
    with open(caminho_saida, 'w', encoding='utf-8') as f:
        json.dump(tabela, f, ensure_ascii=False, indent=4)
    print(f"[+] Tabela de símbolos gerada com sucesso em: {caminho_saida}")


def main():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_config = os.path.join(diretorio_atual, 'configAfd.md')
    caminho_fonte = os.path.join(diretorio_atual, 'codigo.txt')
    caminho_json = os.path.join(diretorio_atual, 'TabSimbolos.json')

    if not os.path.exists(caminho_config):
        print(f"Erro: Arquivo '{caminho_config}' não encontrado.")
        return

    # 1. Carrega as regras do AFD
    estado_inicial, simbolos, estados_finais, transicoes = carregar_afd(caminho_config)

    # 2. Processa o código-fonte e gera o JSON
    if os.path.exists(caminho_fonte):
        print(f"Lendo código-fonte: {os.path.basename(caminho_fonte)}...")
        tabela = processar_codigo_fonte(caminho_fonte, estado_inicial, simbolos, estados_finais, transicoes)
        salvar_tabela_json(tabela, caminho_json)
    else:
        print(f"Arquivo '{caminho_fonte}' não encontrado. Crie o arquivo para testar.")

if __name__ == '__main__':
    main()