# Analisador Léxico com AFD

Projeto em Python que reconhece:

- números inteiros;
- números fracionários;
- números positivos e negativos com `+` e `-`;
- identificadores de variáveis;
- palavras reservadas da linguagem C;
- entradas inválidas por meio do estado morto `QE`.

## Estado de erro QE

O AFD possui:

```text
QE = estado de erro / estado morto / estado poço
```

Quando uma transição não existe, o analisador envia o processamento para `QE`.

Exemplo:

```text
2Variavel

Q0 --2--> Q1
Q1 --V--> QE
QE --a--> QE
QE --r--> QE
...
```

Como `QE` não é estado final, o termo é rejeitado.

## TOKEN x TIPO

Agora:

```text
_oi
Token : IDENTIFICADOR
Tipo  : NOME_VARIAVEL
```

Para números:

```text
15
Token : NUMERO
Tipo  : INTEIRO
```

```text
2.5
Token : NUMERO
Tipo  : FRACIONARIO
```

O TOKEN representa a categoria geral.
O TIPO representa a classificação específica.

## Tabela de símbolos

O CSV usa:

```text
ID;LEXEMA;TOKEN;TIPO;LINHA
```

Exemplo:

```text
1;30;NUMERO;INTEIRO;1
2;-15;NUMERO;INTEIRO;2
3;ABC;IDENTIFICADOR;NOME_VARIAVEL;3
4;2.5;NUMERO;FRACIONARIO;4
```

### ID

Identificador único da linha na tabela de símbolos.

### LEXEMA

Texto exatamente encontrado na entrada.

Exemplos:

```text
30
-15
ABC
_oi
```

### TOKEN

Categoria léxica geral.

Exemplos:

```text
NUMERO
IDENTIFICADOR
```

### TIPO

Subtipo/classificação específica.

Exemplos:

```text
INTEIRO
FRACIONARIO
NOME_VARIAVEL
```

### LINHA

Linha da entrada onde o lexema foi encontrado.

## Executar

```bash
python analisador.py
```

## Mostrar as transições

No terminal:

```text
transicoes 2Variavel
```

ou:

```text
transicoes -2.75
```
