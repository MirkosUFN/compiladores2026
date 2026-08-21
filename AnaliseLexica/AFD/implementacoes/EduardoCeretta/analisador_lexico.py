import csv
caminho = './configAfd.md'

estados = []
estadosFinais = []
simbolos = []
regrasTransicao = []

with open(caminho, encoding='utf-8') as config:
    # A 1ª linha define os estados. O primeiro estado lido é definido como inicial
    estados = config.readline().strip().split(' ')
    estadoInicial = estados[0]
    
    # A 2ª linha define o alfabeto (os símbolos aceitos pelo AFD)
    simbolos = config.readline().strip().split(' ')
    
    # A 3ª linha define quais são os estados finais
    estadosFinais = config.readline().strip().split(' ')
    
    # A partir da 4ª linha, o arquivo contém as regras de transição (ex: q0:a:q1)
    linha = config.readline()
    while linha:
        # Divide a linha caso haja mais de uma regra separada por espaço
        regras = linha.strip().split(' ')
        for r in regras:
            regrasTransicao.append(r)
        linha = config.readline() # Lê a próxima linha até chegar ao fim do arquivo

# Função principal que simula o AFD para reconhecer se um termo é válido
def reconheceTermo(termo):
    # O processamento sempre começa pelo estado inicial definido no arquivo
    estadoAtual = estadoInicial
    numCaracteres = len(termo)
    
    # Itera sobre cada caractere do token recebido
    for i in range(numCaracteres):
        # Passo 1: Verifica se o caractere pertence ao alfabeto da linguagem
        if termo[i] not in simbolos:
            return 'ERRO LEXICO (Símbolo não reconhecido)'
        
        # Passo 2: Monta o padrão de busca (ex: "q0:a") para achar a transição
        padrao = estadoAtual + ':' + termo[i]
        transicao_encontrada = False
        
        # Busca nas regras de transição para ver para qual estado ir agora
        for j in range(len(regrasTransicao)):
            regra = regrasTransicao[j]
            # Se a regra começa com o estado e símbolo atuais...
            if regra.startswith(padrao):
                reg = regra.split(':')
                estadoAtual = reg[2] # ...atualiza o estado atual para o estado de destino
                transicao_encontrada = True
                break # Para a busca, pois o AFD só tem uma transição possível por símbolo
                
        # Passo 3: Se procurou em todas as regras e travou (sem transição válida)
        if not transicao_encontrada:
            return 'ERRO LEXICO (Não há transição para este caractere)'

    # Passo 4: Após processar toda a palavra, verifica se o AFD parou em um estado de aceitação
    for f in range(len(estadosFinais)):
        # Verifica se o estado final listado corresponde ao estado em que paramos
        if estadosFinais[f].startswith(estadoAtual):
            # Retorna o nome/tipo do token
            return estadosFinais[f].split(':')[1]
            
    # Se consumiu a palavra toda mas parou em um estado não final
    return 'ERRO LEXICO (Terminou em estado não-final)'


resultados = []
id_incrementavel = 1

# Abre o arquivo de código fonte para leitura
with open('./numeros.txt', encoding='utf-8') as arquivo:
    # enumerate iterará pelas linhas contando automaticamente (começando em 1)
    for numero_linha, linha in enumerate(arquivo, start=1):
        termo = linha.strip() # Remove quebras de linha e espaços nas pontas
        
        # Pula as linhas que estiverem em branco
        if not termo:
            continue
            
        # Classifica o token chamando a função do AFD
        tipo = reconheceTermo(termo)
        # Salva as 4 colunas formatadas como uma lista dentro da lista 'resultados'
        resultados.append([id_incrementavel, termo, tipo, numero_linha])
        id_incrementavel += 1


caminho_csv = './tabela_simbolos.csv'

with open(caminho_csv, mode='w', newline='', encoding='utf-8-sig') as arquivo_csv:
    # Define o ';' como separador de colunas
    escritor = csv.writer(arquivo_csv, delimiter=';')
    
    # Escreve a primeira linha do arquivo
    escritor.writerow(['ID', 'Token', 'Tipo', 'Linha'])
    
    # Grava todas as linhas de dados analisados de uma só vez no arquivo
    escritor.writerows(resultados)

print(f"Arquivo CSV gerado e salvo com sucesso em: {caminho_csv}")