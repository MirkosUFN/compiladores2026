# Analisador Léxico com AFD e Pilha

O projeto reconhece números inteiros, números fracionários, identificadores
da linguagem C, atribuições, comparações, vírgulas e pontos e vírgulas.

## Reconhecimento com pilha

Cada lexema separado por espaço em branco é colocado em uma pilha de entrada.
Os caracteres são armazenados de modo que o primeiro caractere fique no topo.
O analisador então desempilha **um caractere por vez** e usa esse caractere para
consultar a transição do AFD. Ao esvaziar a pilha, o estado alcançado determina
se o token foi aceito e sua classificação.

Essa abordagem preserva a ordem original do lexema apesar de a pilha ser LIFO.
O comando `transicoes TERMO`, disponível na função interativa legada, também
mostra cada desempilhamento, a transição efetuada e quantos caracteres restam.

A verificação de palavras reservadas é case-sensitive.

## Tabela de símbolos

```text
ID;token;tipo;linha;coluna
```

Exemplo:

```text
1;30;INTEIRO;1;1
2;-30;INTEIRO;1;4
3;3.5;FRACIONARIO;2;1
4;abc;NOMEVARIAVEL;2;7
5;_oi;NOMEVARIAVEL;3;3
```

## Execução

```bash
python analisador.py
```

O programa lê `input.c` e grava `tabela_simbolos.csv` na mesma pasta. Os
tokens precisam estar separados por espaços em branco. Cada token recebe sua
própria pilha. Linha e coluna são registradas a partir de 1.

As categorias reconhecidas são `INTEIRO`, `FRACIONARIO`, `NOMEVARIAVEL`,
`ATRIBUIÇÃO`, `SINAL_COMPARAÇÃO`, `VÍRGULA` e `PONTO_VIRGULA`.
