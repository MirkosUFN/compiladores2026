# Analisador Léxico — vários tokens por linha — Romeo Noro Guterres

## Como funciona

1. O AFD é carregado de `AFD_config.txt` (mesmo formato do `configAfd.md`).
2. Cada linha de `input.c` é varrida caractere a caractere. Ao achar espaço em
   branco o token atual termina, é submetido ao AFD e o AFD volta para `Q0`.
3. A coluna registrada é a do **primeiro caractere** do token (linhas e colunas
   começam em 1).
4. Tokens aceitos vão para `tabela_simbolos.csv`; os rejeitados são exibidos
   como erro léxico com linha, coluna e motivo.

## AFD

| Estado | Significado               | Final? | Token            |
|--------|---------------------------|--------|------------------|
| Q0     | inicial                   |        |                  |
| Q1     | dígitos                   | sim    | INTEIRO          |
| Q2     | dígitos + `.`             |        |                  |
| Q3     | dígitos + `.` + dígitos   | sim    | FRACIONARIO      |
| Q4     | sinal `+` / `-`           |        |                  |
| Q5     | letra/`_` (letra/díg/`_`)*| sim    | NOMEVARIAVEL     |
| Q6     | `=`                       | sim    | ATRIBUIÇÃO       |
| Q7     | `==` `>=` `<=` `!=`       | sim    | SINAL_COMPARAÇÃO |
| Q8     | `<` `>`                   | sim    | SINAL_COMPARAÇÃO |
| Q9     | `!`                       |        |                  |
| Q10    | `,`                       | sim    | VÍRGULA          |
| Q11    | `;`                       | sim    | PONTO_VIRGULA    |

## Execução

```bash
python analisador.py                       # AFD_config.txt + input.c
python analisador.py AFD_config.txt outro.c
```

Saída (`tabela_simbolos.csv`):

```text
ID;token;tipo;linha;coluna
1;int;NOMEVARIAVEL;1;1
2;idade;NOMEVARIAVEL;1;5
3;=;ATRIBUIÇÃO;1;11
4;20;INTEIRO;1;13
...
```

O `input.c` de exemplo tem de propósito `(`, `)` e `+` sozinho, que não fazem
parte dos tokens pedidos, para mostrar o relatório de erros léxicos.
Palavras reservadas ainda não são separadas nesta etapa (`int` sai como
NOMEVARIAVEL).
