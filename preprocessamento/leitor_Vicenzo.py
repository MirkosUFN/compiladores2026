import sys

print("Iniciando o limpador de comentarios...")

nome_entrada = input("Digite o nome do arquivo para ler: ")
nome_saida = input("Digite o nome do arquivo para salvar: ")

try:
    arquivo_leitura = open(nome_entrada, "r", encoding="utf-8")
    conteudo = arquivo_leitura.readlines()
    arquivo_leitura.close()
except:
    print("Erro ao abrir o arquivo. Verifique se ele esta na mesma pasta.")
    sys.exit()

linhas_novas = []

for linha in conteudo:
    posicao = linha.find("#")
    if posicao != -1:
        linha = linha[:posicao] + "\n"
    
    if linha.strip() != "":
        linhas_novas.append(linha)

arquivo_escrita = open(nome_saida, "w", encoding="utf-8")
arquivo_escrita.writelines(linhas_novas)
arquivo_escrita.close()

print("Pronto! Arquivo limpo com sucesso.")