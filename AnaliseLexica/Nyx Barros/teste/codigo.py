import os

from codigo.afd import AFD

afd = AFD('config/configAfd.md' if os.path.exists('config/configAfd.md') else 'config/configAfd.txt')

with open('teste/teste.txt', 'r') as arquivo:
    for linha in arquivo:
        linha = linha.strip()
        if linha:
            print(linha, '→', afd.reconhecer_termo(linha))