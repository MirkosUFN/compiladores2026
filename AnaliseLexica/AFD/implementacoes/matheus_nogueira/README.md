# Analisador Léxico com AFD

O projeto reconhece números inteiros, números fracionários e identificadores
da linguagem C.

A verificação de palavras reservadas é case-sensitive.

## Tabela de símbolos

```text
ID;TOKEN;TIPO;LINHA
```

Exemplo:

```text
1;30;INTEIRO;1
2;-30;INTEIRO;2
3;3.5;FRACIONARIO;3
4;abc;NOME_VARIAVEL;4
5;_oi;NOME_VARIAVEL;5
```

## Execução

```bash
python analisador.py
```
