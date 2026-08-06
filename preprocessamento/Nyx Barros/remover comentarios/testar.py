import remover_comentarios

arquivos = ['teste1', 'teste2', 'teste3', 'teste4', 'teste5']

for i in arquivos:
    pasta = 'testes/remover_comentario/'
    remover_comentarios.processar_arquivo(pasta+i, pasta+i+'-resposta')