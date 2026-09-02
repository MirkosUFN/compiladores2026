# Analisador Léxico com AFD

O projeto reconhece números inteiros, números fracionários e identificadores
da linguagem C.

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
tokens precisam estar separados por espaços em branco. Linha e coluna são
registradas a partir de 1.

As categorias reconhecidas são `INTEIRO`, `FRACIONARIO`, `NOMEVARIAVEL`,
`ATRIBUIÇÃO`, `SINAL_COMPARAÇÃO`, `VÍRGULA` e `PONTO_VIRGULA`.
