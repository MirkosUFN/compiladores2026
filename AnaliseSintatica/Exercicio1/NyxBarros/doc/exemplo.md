# EXEMPLO DA ANÁLISE DE UM CÓDIGO

## Código analizado

```C
if(x>0){
    if(y>0){z=0;}
}
```

## Tabela de simbolos


| ID | token | tipo                  | linha | coluna |
|----|-------|-----------------------|-------|--------|
|  1 | if    | PALAVRA_RESERVADA IF  |     1 |      0 |
|  2 | (     | ABRE_PARENTESES       |     1 |      2 |
|  3 | x     | NOME_VARIAVEL         |     1 |      3 |
|  4 | >     | COMPARATIVO           |     1 |      4 |
|  5 | 0     | INTEIRO               |     1 |      5 |
|  6 | )     | FECHA_PARENTESES      |     1 |      6 |
|  7 | {     | ABRE_CHAVES           |     1 |      7 |
|  8 | if    | PALAVRA_RESERVADA IF  |     2 |      4 |
|  9 | (     | ABRE_PARENTESES       |     2 |      6 |
| 10 | y     | NOME_VARIAVEL         |     2 |      7 |
| 11 | >     | COMPARATIVO           |     2 |      8 |
| 12 | 0     | INTEIRO               |     2 |      9 |
| 13 | )     | FECHA_PARENTESES      |     2 |     10 |
| 14 | {     | ABRE_CHAVES           |     2 |     11 |
| 15 | z     | NOME_VARIAVEL         |     2 |     12 |
| 16 | =     | ATRIBUICAO            |     2 |     13 |
| 17 | 0     | INTEIRO               |     2 |     14 |
| 18 | ;     | PONTO_VIRGULA         |     2 |     15 |
| 19 | }     | FECHA_CHAVES          |     2 |     16 |
| 20 | }     | FECHA_CHAVES          |     3 |      0 |

## Árvore de derivação

```txt
SIF
├── [PR:if] ("if")
├── [ABRE PARENTESES] ("(")
├── Condicao
│   └── Compara
│       ├── [NOME VARIÁVEL] ("x")
│       ├── [COMPARACAO] (">")
│       └── Valor
│           └── [INTEIRO] ("0")
├── [FECHA PARENTESES] (")")
├── [ABRE CHAVES] ("{")
├── Bloco
│   └── SIF
│       ├── [PR:if] ("if")
│       ├── [ABRE PARENTESES] ("(")
│       ├── Condicao
│       │   └── Compara
│       │       ├── [NOME VARIÁVEL] ("y")
│       │       ├── [COMPARACAO] (">")
│       │       └── Valor
│       │           └── [INTEIRO] ("0")
│       ├── [FECHA PARENTESES] (")")
│       ├── [ABRE CHAVES] ("{")
│       ├── Bloco
│       │   └── AtribuirInt  <-- (Inferido para z = 0;)
│       │       ├── [NOME VARIÁVEL] ("z")
│       │       ├── [ATRIBUICAO] ("=")
│       │       ├── [INTEIRO] ("0")
│       │       └── [PONTO E VIRGULA] (";")
│       └── [FECHA CHAVE] ("}")
└── [FECHA CHAVE] ("}")
```