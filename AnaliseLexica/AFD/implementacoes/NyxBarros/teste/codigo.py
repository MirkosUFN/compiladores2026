import os

from codigo.tabela_simbolos import TabelaSimbolos

arquivo_config_afd = 'config/configAfd.md' if os.path.exists('config/configAfd.md') else 'config/configAfd.txt'
arquivo_teste = 'teste/teste.txt'

# Criar a tabela e analisar automaticamente
tabela_simbolos = TabelaSimbolos(arquivo_config_afd, arquivo_teste)
tabela_simbolos.gerar_arquivo_csv()
tabela_simbolos.gerar_arquivo_json()