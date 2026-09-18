# Exercício 1 — Análise Sintática

Esta implementação atende ao enunciado de `AnaliseSintatica/Exercicio1`.

## Sintaxe

Os tipos aceitos são `int`, `char`, `float`, `double`, `void` e `boolean`.
Cada variável pode ser declarada sem inicialização ou com uma inicialização
simples:

```c
int numero;
int numero = 10;
int a = 1, b = 2, c;
float media = 7.5;
boolean ativo = true;
```

A gramática está registrada em [sintaxe.txt](sintaxe.txt). A regra de
inicialização é:

```text
DECLARADOR -> NOMEVARIAVEL | NOMEVARIAVEL ATRIBUICAO VALOR
VALOR -> INTEIRO | FRACIONARIO | NOMEVARIAVEL | PR:TRUE | PR:FALSE
```

`DeclaraMultiplo` pode repetir indefinidamente o trecho `, DECLARADOR`.

## Execução

Na pasta desta implementação, execute:

```bash
python3 analisador_sintatico.py
```

O programa mostra os tokens, informa se cada declaração foi aceita e grava os
tokens reconhecidos em `tabela_simbolos.csv`.
