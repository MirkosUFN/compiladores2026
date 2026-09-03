import os

from codigo.afd_copy import AFD

arquivo_config_afd = 'config/configAfd.md' if os.path.exists('config/configAfd.md') else 'config/configAfd.txt'
arquivo_teste = 'teste/teste.txt'

# Criar a tabela e analisar automaticamente
tabela_simbolos = AFD(arquivo_config_afd)
tabela_simbolos.analisar_arquivo(arquivo_teste)
tabela_simbolos.gerar_arquivo_csv()
tabela_simbolos.gerar_arquivo_json()
tabela_simbolos.gerar_arquivo_mk()
