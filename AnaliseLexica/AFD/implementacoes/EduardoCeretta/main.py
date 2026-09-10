import csv

# Conjunto com as palavras reservadas da linguagem C
palavras_reservadas_c = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do', 
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if', 
    'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 
    'static', 'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 
    'volatile', 'while'
}

caminho = './AFD_config.txt'

estados = []
estadosFinais = []
simbolos = []
regrasTransicao = []

# Lê as configurações do AFD
with open(caminho, encoding='utf-8') as config:
    estados = config.readline().strip().split(' ')
    estadoInicial = estados[0]
    
    simbolos = config.readline().strip().split(' ')
    estadosFinais = config.readline().strip().split(' ')
    
    linha = config.readline()
    while linha:
        regras = linha.strip().split(' ')
        for r in regras:
            if r:
                regrasTransicao.append(r)
        linha = config.readline()

def reconheceTermo(termo):
    estadoAtual = estadoInicial
    numCaracteres = len(termo)
    
    for i in range(numCaracteres):
        if termo[i] not in simbolos:
            return 'ERRO LEXICO (Símbolo não reconhecido)'
        
        padrao = estadoAtual + ':' + termo[i]
        transicao_encontrada = False
        
        for j in range(len(regrasTransicao)):
            regra = regrasTransicao[j]
            if regra.startswith(padrao):
                reg = regra.split(':')
                estadoAtual = reg[2]
                transicao_encontrada = True
                break
                
        if not transicao_encontrada:
            return 'ERRO LEXICO (Não há transição para este caractere)'

    for f in range(len(estadosFinais)):
        if estadosFinais[f].startswith(estadoAtual):
            return estadosFinais[f].split(':')[1]
            
    return 'ERRO LEXICO (Terminou em estado não-final)'


resultados = []
id_incrementavel = 1

with open('./input.c', encoding='utf-8') as arquivo:
    for numero_linha, linha in enumerate(arquivo, start=1):
        linha_pura = linha.strip('\n') 
        tokens = [t for t in linha_pura.split(' ') if t]
        
        coluna_atual = 1 
        
        for termo in tokens:
            indice_coluna = linha_pura.find(termo, coluna_atual - 1)
            coluna_final = indice_coluna + 1 
            
            # Reconhece o tipo original pelo AFD (provavelmente NOMEVARIAVEL para textos)
            tipo = reconheceTermo(termo)
            
            # ATUALIZAÇÃO: Verifica se é uma palavra reservada da linguagem C
            if tipo == 'NOMEVARIAVEL' and termo in palavras_reservadas_c:
                tipo = 'PALAVRA_RESERVADA'
            
            resultados.append([id_incrementavel, termo, tipo, numero_linha, coluna_final])
            
            id_incrementavel += 1
            coluna_atual = indice_coluna + len(termo)

caminho_csv = './tabela_simbolos.csv'

with open(caminho_csv, mode='w', newline='', encoding='utf-8-sig') as arquivo_csv:
    escritor = csv.writer(arquivo_csv, delimiter=';')
    escritor.writerow(['ID', 'Token', 'Tipo', 'Linha', 'Coluna'])
    escritor.writerows(resultados)

print(f"Tabela de Símbolos gerada com sucesso em: {caminho_csv}")