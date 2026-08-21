import csv
import os
import string

def carregar_configuracao_afd(caminho_arquivo):
    """Lê o arquivo configAfd.md e estrutura os componentes do AFD."""
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        linhas = [linha.strip() for linha in f.readlines() if linha.strip()]

    if len(linhas) < 4:
        raise ValueError("O arquivo de configuração não possui as 4 linhas obrigatórias.")

    estado_inicial = linhas[0].split()[0]

    estados_finais = {}
    for item in linhas[2].split():
        estado, tipo = item.split(':')
        estados_finais[estado] = tipo

    transicoes = {}
    for linha in linhas[3:]:
        regras = linha.split()
        for regra in regras:
            if ':' in regra:
                est_orig, simbolo, est_dest = regra.split(':')
                transicoes[(est_orig, simbolo)] = est_dest

    return estado_inicial, estados_finais, transicoes

def simular_afd(token, estado_inicial, estados_finais, transicoes):
    """Roda a string no AFD montado a partir das regras de transição."""
    estado_atual = estado_inicial
    
    for char in token:
        if (estado_atual, char) in transicoes:
            estado_atual = transicoes[(estado_atual, char)]
        else:
            return "ERRO"
            
    return estados_finais.get(estado_atual, "ERRO")

def analisar_codigo_fonte(codigo, estado_inicial, estados_finais, transicoes):
    """Gera a tabela de símbolos simulando cada token no AFD."""
    tabela = []
    id_token = 1
    linhas = codigo.strip().split('\n')
    
    for num_linha, linha in enumerate(linhas, start=1):
        tokens = linha.split()
        for token in tokens:
            tipo = simular_afd(token, estado_inicial, estados_finais, transicoes)
            tabela.append({
                'ID': id_token,
                'TOKEN': token,
                'TIPO': tipo,
                'LINHA': num_linha
            })
            id_token += 1
            
    return tabela

def exibir_e_salvar_tabela(tabela, arquivo_csv="tabela_simbolos.csv"):
    """Exibe no console igual à imagem fornecida (com bordas) e salva em CSV."""
    print("┌───────────────────────────────────────────────┐")
    print("│              Tabela de Símbolos               │")
    print("├──────┬─────────────────┬──────────────┬───────┤")
    print("│ ID   │ TOKEN           │ TIPO         │ LINHA │")
    print("├──────┼─────────────────┼──────────────┼───────┤")
    
    for t in tabela:
        print(f"│ {t['ID']:<4} │ {t['TOKEN']:<15} │ {t['TIPO']:<12} │ {t['LINHA']:<5} │")
        
    print("└──────┴─────────────────┴──────────────┴───────┘")
    
    with open(arquivo_csv, mode='w', newline='', encoding='utf-8') as f:
        escritor = csv.writer(f, delimiter=';')
        escritor.writerow(['ID', 'TOKEN', 'TIPO', 'LINHA'])
        for t in tabela:
            escritor.writerow([t['ID'], t['TOKEN'], t['TIPO'], t['LINHA']])
    print(f"\nArquivo '{arquivo_csv}' gerado com sucesso!")

# =================================================================
# EXECUÇÃO DO PROGRAMA
# =================================================================
if __name__ == "__main__":
    arquivo_config = "configAfd.md"
    arquivo_entrada = "numeros.txt"

    # 1. Cria o arquivo de configuração dinamicamente com TODAS as letras do alfabeto
    todas_letras = string.ascii_lowercase + string.ascii_uppercase
    
    regras_q0_letras = " ".join([f"Q0:{letra}:Q5" for letra in todas_letras])
    regras_q5_letras = " ".join([f"Q5:{letra}:Q5" for letra in todas_letras])

    conteudo_config = f"""Q0 Q1 Q2 Q3 Q4 Q5
0 1 2 3 4 5 6 7 8 9 . + - a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z _
Q1:INT Q3:FRAC Q5:NOMEVARIAVEL
Q0:0:Q1 Q0:1:Q1 Q0:2:Q1 Q0:3:Q1 Q0:4:Q1 Q0:5:Q1 Q0:6:Q1 Q0:7:Q1 Q0:8:Q1 Q0:9:Q1
Q0:-:Q4 Q0:+:Q4 Q4:0:Q3 Q4:1:Q3 Q4:2:Q3 Q4:3:Q3 Q4:4:Q3 Q4:5:Q3 Q4:6:Q3 Q4:7:Q3 Q4:8:Q3 Q4:9:Q3
Q1:0:Q1 Q1:1:Q1 Q1:2:Q1 Q1:3:Q1 Q1:4:Q1 Q1:5:Q1 Q1:6:Q1 Q1:7:Q1 Q1:8:Q1 Q1:9:Q1 Q1:.:Q2
Q2:0:Q3 Q2:1:Q3 Q2:2:Q3 Q2:3:Q3 Q2:4:Q3 Q2:5:Q3 Q2:6:Q3 Q2:7:Q3 Q2:8:Q3 Q2:9:Q3
Q3:0:Q3 Q3:1:Q3 Q3:2:Q3 Q3:3:Q3 Q3:4:Q3 Q3:5:Q3 Q3:6:Q3 Q3:7:Q3 Q3:8:Q3 Q3:9:Q3
{regras_q0_letras} Q0:_:Q5
{regras_q5_letras} Q5:0:Q5 Q5:1:Q5 Q5:2:Q5 Q5:3:Q5 Q5:4:Q5 Q5:5:Q5 Q5:6:Q5 Q5:7:Q5 Q5:8:Q5 Q5:9:Q5 Q5:_:Q5
"""
    # Força a reescrita do arquivo para garantir que as novas regras sejam aplicadas
    with open(arquivo_config, "w", encoding='utf-8') as f:
        f.write(conteudo_config)

    # 2. Carrega as configurações do AFD
    estado_ini, estados_fin, regras_trans = carregar_configuracao_afd(arquivo_config)

    # 3. Lê o arquivo numeros.txt
    if os.path.exists(arquivo_entrada):
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            codigo_fonte = f.read()
            
        # 4. Analisa e gera a tabela
        if codigo_fonte.strip():
            tabela_resultados = analisar_codigo_fonte(codigo_fonte, estado_ini, estados_fin, regras_trans)
            exibir_e_salvar_tabela(tabela_resultados)
        else:
            print(f"O arquivo '{arquivo_entrada}' está vazio.")
    else:
        print(f"ERRO: O arquivo '{arquivo_entrada}' não foi encontrado.")
