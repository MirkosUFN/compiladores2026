import os

from code.afd import AFD



arquivo_config_afd = 'config_c/configAfd.md' if os.path.exists('config_c/configAfd.md') else 'config_c/configAfd.txt'
arquivo_palavras_reservadas = 'config_c/palavrasReservadas.txt'
arquivo_teste = 'teste/teste.txt'

# Criar a tabela e analisar automaticamente
tabela_simbolos = AFD(arquivo_config_afd, arquivo_palavras_reservadas)
tabela_simbolos.analisar_arquivo(arquivo_teste)
tabela_simbolos.gerar_arquivo_csv()
tabela_simbolos.gerar_arquivo_json()
tabela_simbolos.gerar_arquivo_mk()
