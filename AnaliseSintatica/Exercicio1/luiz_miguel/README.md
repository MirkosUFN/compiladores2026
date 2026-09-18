# Exercício 1 — Análise Sintática

Esta implementação atende ao enunciado de **AnaliseSintatica/Exercicio1**, com suporte a literais numéricos, booleanos, caracteres (`'...'` / `''`) e cadeias de caracteres (`"..."` / `""`), reaproveitando o conceito e a visualização em tabela de [`analise_lexica/gerador_tabela_afd.py`](../analise_lexica/gerador_tabela_afd.py).

## Sintaxe

Os tipos aceitos são `int`, `char`, `float`, `double`, `void` e `boolean`. Cada variável pode ser declarada sem inicialização ou com inicialização simples:

```c
int numero;
int numero = 10;
int a = 1, b = 2, c;
float media = 7.5;
boolean ativo = true;
char letra = 'a';
char vazio = '';
char mensagem = "compiladores";
char texto_vazio = "";
```

A gramática está registrada em [`sintaxe.txt`](sintaxe.txt). A regra de inicialização é:

```text
# Tipos definidos no enunciado
[TIPO] -> PR:INT | PR:CHAR | PR:FLOAT | PR:DOUBLE | PR:VOID | PR:BOOLEAN

# Nova sintaxe: cada variável pode ser declarada sem valor ou inicializada
[VALOR] -> INTEIRO | FRACIONARIO | NOMEVARIAVEL | PR:TRUE | PR:FALSE | LITERAL_CARACTERE | LITERAL_TEXTO
[INICIALIZACAO] -> ATRIBUICAO VALOR
[DECLARADOR] -> NOMEVARIAVEL | NOMEVARIAVEL INICIALIZACAO

Declara -> TIPO DECLARADOR PV | TIPO DECLARADOR DeclaraMultiplo PV
DeclaraMultiplo -> VG DECLARADOR | VG DECLARADOR DeclaraMultiplo
```

`DeclaraMultiplo` pode repetir indefinidamente o trecho `, DECLARADOR`.

---

## Execução

Na pasta desta implementação, execute:

```bash
python3 analisador_sintatico.py
```
*(ou `python analisador_sintatico.py` no Windows)*

O programa mostra:
1. Os tokens e o resultado de cada linha analisada.
2. A **Tabela de Símbolos (Léxica)** formatada no terminal (estilo `gerador_tabela_afd.py`).
3. O **Resumo da Análise Sintática** formatado em tabela.
4. Grava os tokens reconhecidos em [`tabela_simbolos.csv`](tabela_simbolos.csv).

---

## Exemplo de Saída em Tabela

### Tabela de Símbolos (Léxica)
```text
=== TABELA DE SÍMBOLOS (ANÁLISE LÉXICA) ===
+----+-------------------+-------------------+-------+--------+
| ID | token             | tipo              | linha | coluna |
+----+-------------------+-------------------+-------+--------+
| 30 | char              | PR:CHAR           | 6     | 1      |
| 31 | letra             | NOMEVARIAVEL      | 6     | 6      |
| 32 | =                 | ATRIBUICAO        | 6     | 12     |
| 33 | 'a'               | LITERAL_CARACTERE | 6     | 14     |
| 34 | ;                 | PONTO_VIRGULA     | 6     | 17     |
| 35 | char              | PR:CHAR           | 7     | 1      |
| 36 | vazio             | NOMEVARIAVEL      | 7     | 6      |
| 37 | =                 | ATRIBUICAO        | 7     | 12     |
| 38 | ''                | LITERAL_CARACTERE | 7     | 14     |
| 39 | ;                 | PONTO_VIRGULA     | 7     | 16     |
| 40 | char              | PR:CHAR           | 8     | 1      |
| 41 | mensagem          | NOMEVARIAVEL      | 8     | 6      |
| 42 | =                 | ATRIBUICAO        | 8     | 15     |
| 43 | "compiladores"    | LITERAL_TEXTO     | 8     | 17     |
| 44 | ;                 | PONTO_VIRGULA     | 8     | 31     |
+----+-------------------+-------------------+-------+--------+
```

### Resumo da Análise Sintática
```text
=== RESUMO DA ANÁLISE SINTÁTICA ===
+-------+---------------------------------+------------+------------------+-----------+---------------------------+
| Linha | Código                          | Tipo       | Regra            | Status    | Declaradores              |
+-------+---------------------------------+------------+------------------+-----------+---------------------------+
| 1     | int numero;                     | PR:INT     | DECLARA          | ACEITA    | numero                    |
| 2     | int numero = 10;                | PR:INT     | DECLARA          | ACEITA    | numero = 10               |
| 3     | int a = 1, b = 2, c;            | PR:INT     | DECLARA_MULTIPLO | ACEITA    | a = 1, b = 2, c           |
| 4     | float media = 7.5;              | PR:FLOAT   | DECLARA          | ACEITA    | media = 7.5               |
| 5     | boolean ativo = true;           | PR:BOOLEAN | DECLARA          | ACEITA    | ativo = true              |
| 6     | char letra = 'a';               | PR:CHAR    | DECLARA          | ACEITA    | letra = 'a'               |
| 7     | char vazio = '';                | PR:CHAR    | DECLARA          | ACEITA    | vazio = ''                |
| 8     | char mensagem = "compiladores"; | PR:CHAR    | DECLARA          | ACEITA    | mensagem = "compiladores" |
| 9     | char texto_vazio = "";          | PR:CHAR    | DECLARA          | ACEITA    | texto_vazio = ""          |
| 10    | int erro_atribuicao = ;         | PR:INT     | -                | REJEITADA | -                         |
| 11    | float = 10;                     | PR:FLOAT   | -                | REJEITADA | -                         |
| 12    | double sem_ponto_virgula        | PR:DOUBLE  | -                | REJEITADA | sem_ponto_virgula         |
+-------+---------------------------------+------------+------------------+-----------+---------------------------+
```

---

## Estrutura dos Arquivos

- [`analisador_sintatico.py`](analisador_sintatico.py): Analisador léxico e sintático com visualização em tabela e exportação para CSV.
- [`sintaxe.txt`](sintaxe.txt): Registro formal das produções da gramática.
- [`input.c`](input.c): Arquivo de entrada com os códigos de teste.
- [`tabela_simbolos.csv`](tabela_simbolos.csv): Tabela de símbolos gerada após a execução.
