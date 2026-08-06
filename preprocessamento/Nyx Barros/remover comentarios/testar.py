import remover_comentarios

arquivos = ['teste1', 'teste2', 'teste3', 'teste4', 'teste5']

for i in arquivos:
    arquivo = 'testes/remover_comentario/'+i
    remover_comentarios.processar_arquivo(arquivo, arquivo+'-resposta')
