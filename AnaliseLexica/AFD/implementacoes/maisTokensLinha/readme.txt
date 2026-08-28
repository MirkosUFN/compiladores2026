Implemente uma modificação no Analisador Léxico de forma que ele reconheça mais de um token por linha e construa a tabela de símbolos corretamente.
A tabela de símbolos deve ser atualizada, agora contando com as seguintes colunas: ID, token, tipo, linha e coluna.
Os tipos de tokens que deve ser reconhecido nessa atualização são:
INTEIRO
FRACIONARIO
NOMEVARIAVEL
ATRIBUIÇÃO
SINAL_COMPARAÇÃO
VÍRGULA
PONTO_VIRGULA

Cada aluno deve fazer o commit de uma pasta com seu nome e a implementação correspondente junto com o arquivo AFD_config.txt
Eu irei testar o input com um arquivo chamado input.c contendo vários tokens por linha e mais de uma linha avaliando a tabela de símbolos resultante.
*os tokens nesse arquivo estarão separados por espaço em branco*
