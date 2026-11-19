# Mais tokens por linha — Bruno Difante

Execute `python3 analisador_lexico.py`. O script lê `input.c` e
`AFD_config.txt` e gera `tabela_simbolos.csv` com ID, token, tipo,
linha e coluna. Para usar outros arquivos, passe primeiro o caminho
da configuração e depois o caminho da entrada.

Separe os tokens por espaço em branco, como no enunciado. As posições
começam em 1. A coluna conta caracteres da linha original, incluindo
tabulações. Um termo que o AFD rejeita recebe o tipo `NAO_RECONHECIDO`.
