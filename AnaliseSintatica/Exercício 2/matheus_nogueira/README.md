# Exercício 2 — Balanceamento de delimitadores

Esta implementação valida os tokens `()`, `{}` e `[]` conforme o enunciado
do Exercício 2. Além de conferir a quantidade, o analisador verifica se os
delimitadores estão aninhados na ordem correta.

## Tabela de símbolos

A tabela é gravada em `tabela_simbolos.csv` com as colunas:

```text
ID;token;tipo;linha;coluna;Ref
```

Para um token de fechamento, `Ref` recebe o `ID` do token de abertura
correspondente. Os tokens de abertura e os demais tokens deixam essa coluna
vazia.

## Execução

Na pasta desta implementação, execute:

```bash
python analisador_sintatico.py
```

O programa lê `input.c`, mostra os tokens no terminal, valida os delimitadores
e gera `tabela_simbolos.csv` na mesma pasta.

## Arquivos

- `analisador_sintatico.py`: tokenização, validação com pilha e geração da tabela;
- `input.c`: entrada usada no exemplo;
- `sintaxe.txt`: representação das regras do exercício;
- `tabela_simbolos.csv`: resultado gerado após a execução.

Um fechamento sem abertura, uma abertura sem fechamento ou um par de tipos
diferentes faz a análise ser rejeitada.
