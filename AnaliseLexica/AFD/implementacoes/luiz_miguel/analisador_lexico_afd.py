import os

def carregar_afd(caminho_config):
    """
    Carrega as configurações do AFD a partir de um arquivo com o seguinte formato:
    - 1ª linha: Estados separados por espaço (o primeiro é o estado inicial)
    - 2ª linha: Símbolos do alfabeto separados por espaço
    - 3ª linha: Estados finais e seus tokens no formato Estado:TOKEN separados por espaço
    - 4ª linha em diante: Regras de transição no formato EstadoOrigem:Simbolo:EstadoDestino
    """
    with open(caminho_config, 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]

    if len(linhas) < 3:
        raise ValueError("Arquivo de configuração do AFD inválido ou incompleto.")

    estados = linhas[0].split()
    estado_inicial = estados[0]
    simbolos = set(linhas[1].split())

    # Mapeamento de estado final -> Categoria/Token (ex: {'Q1': 'INTEIRO', 'Q3': 'FRACIONÁRIO'})
    estados_finais = {}
    for ef in linhas[2].split():
        if ':' in ef:
            est, token = ef.split(':', 1)
            estados_finais[est] = token

    # Mapeamento de transições: (estado_atual, simbolo) -> proximo_estado
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
    Processa um termo pelo AFD e retorna o resultado no formato 'termo:TOKEN'
    ou mensagem de erro caso o termo não seja aceito.
    """
    estado_atual = estado_inicial

    for caractere in termo:
        if caractere not in simbolos:
            return f"Erro em '{termo}': Símbolo '{caractere}' não pertence ao alfabeto."
        
        chave = (estado_atual, caractere)
        if chave in transicoes:
            estado_atual = transicoes[chave]
        else:
            return f"Erro em '{termo}': Transição inválida a partir do estado '{estado_atual}' com o símbolo '{caractere}'."

    if estado_atual in estados_finais:
        return f"{termo}:{estados_finais[estado_atual]}"
    else:
        return f"Erro em '{termo}': Termo terminou no estado não-final '{estado_atual}'."

def main():
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    caminho_config = os.path.join(diretorio_atual, 'configAfd.md')
    caminho_numeros = os.path.join(diretorio_atual, 'numeros.txt')

    # 1. Carrega as regras do AFD a partir do arquivo de configuração
    estado_inicial, simbolos, estados_finais, transicoes = carregar_afd(caminho_config)

    print("=== Reconhecimento de Termos via AFD ===")

    # 2. Se houver o arquivo numeros.txt, processa as linhas dele primeiro
    if os.path.exists(caminho_numeros):
        print(f"\n--- Lendo termos do arquivo '{os.path.basename(caminho_numeros)}' ---")
        with open(caminho_numeros, 'r', encoding='utf-8') as f:
            for linha in f:
                termo = linha.strip()
                if termo:
                    resultado = reconhecer_termo(termo, estado_inicial, simbolos, estados_finais, transicoes)
                    print(resultado)

    # 3. Modo Interativo: Permite que você digite qualquer termo diretamente no terminal
    print("\n--- Modo Interativo (Digite seus termos abaixo) ---")
    print("Digite um termo para testar ou 'sair' para encerrar.\n")

    while True:
        try:
            entrada = input("Digite o termo: ").strip()
            if entrada.lower() in ('sair', 'exit'):
                print("Encerrando analisador léxico.")
                break
            if not entrada:
                continue
            
            resultado = reconhecer_termo(entrada, estado_inicial, simbolos, estados_finais, transicoes)
            print(f"Resultado: {resultado}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nEncerrando...")
            break

if __name__ == '__main__':
    main()
