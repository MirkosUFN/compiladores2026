# Exercício 1 — Análise Sintática

Esta implementação atende ao enunciado de **AnaliseSintatica/Exercicio1**, com suporte a literais numéricos, booleanos, caracteres (`'...'` / `''`) e cadeias de caracteres (`"..."` / `""`), exibindo a **Árvore de Derivação Sintática** e o **Resumo da Análise Sintática** formatado em tabela ASCII.

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
int nome, idade=23, filhos=3;
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
1. Os tokens de cada linha.
2. A **Árvore de Derivação** para cada declaração aceita.
3. O **Resumo da Análise Sintática** formatado em tabela ASCII.
4. Grava os tokens reconhecidos no arquivo [`tabela_simbolos.csv`](tabela_simbolos.csv).

---

## Exemplos da Árvore de Derivação

### Declaração Simples com Inicialização
Para `int numero = 10;`:
```text
Árvore de Derivação:
  └── Declara
      ├── [TIPO]: PR:INT
      ├── DECLARADOR
      │   ├── [NOMEVARIAVEL]: numero
      │   └── INICIALIZACAO
      │       ├── [ATRIBUICAO]: =
      │       └── [VALOR]: 10
      └── [PV]: ;
```

### Declaração Múltipla Mista
Para `int nome, idade=23, filhos=3;`:
```text
Árvore de Derivação:
  └── Declara
      ├── [TIPO]: PR:INT
      ├── DECLARADOR
      │   └── [NOMEVARIAVEL]: nome
      ├── DeclaraMultiplo
      │   ├── [VG]: ,
      │   ├── DECLARADOR
      │   │   ├── [NOMEVARIAVEL]: idade
      │   │   └── INICIALIZACAO
      │   │       ├── [ATRIBUICAO]: =
      │   │       └── [VALOR]: 23
      │   └── DeclaraMultiplo
      │       ├── [VG]: ,
      │       └── DECLARADOR
      │           ├── [NOMEVARIAVEL]: filhos
      │           └── INICIALIZACAO
      │               ├── [ATRIBUICAO]: =
      │               └── [VALOR]: 3
      └── [PV]: ;
```

Para `int a = 1, b = 2, c;`:
```text
Árvore de Derivação:
  └── Declara
      ├── [TIPO]: PR:INT
      ├── DECLARADOR
      │   ├── [NOMEVARIAVEL]: a
      │   └── INICIALIZACAO
      │       ├── [ATRIBUICAO]: =
      │       └── [VALOR]: 1
      ├── DeclaraMultiplo
      │   ├── [VG]: ,
      │   ├── DECLARADOR
      │   │   ├── [NOMEVARIAVEL]: b
      │   │   └── INICIALIZACAO
      │       │   ├── [ATRIBUICAO]: =
      │       │   └── [VALOR]: 2
      │   └── DeclaraMultiplo
      │       ├── [VG]: ,
      │       └── DECLARADOR
      │           └── [NOMEVARIAVEL]: c
      └── [PV]: ;
```

---

## Exemplo de Saída da Tabela Sintática

```text
=== RESUMO DA ANÁLISE SINTÁTICA ===
+-------+---------------------------------+------------+------------------+-----------+------------------------------+
| Linha | Código                          | Tipo       | Regra            | Status    | Declaradores                 |
+-------+---------------------------------+------------+------------------+-----------+------------------------------+
| 1     | int numero;                     | PR:INT     | DECLARA          | ACEITA    | numero                       |
| 2     | int numero = 10;                | PR:INT     | DECLARA          | ACEITA    | numero = 10                  |
| 3     | int a = 1, b = 2, c;            | PR:INT     | DECLARA_MULTIPLO | ACEITA    | a = 1, b = 2, c              |
| 4     | float media = 7.5;              | PR:FLOAT   | DECLARA          | ACEITA    | media = 7.5                  |
| 5     | boolean ativo = true;           | PR:BOOLEAN | DECLARA          | ACEITA    | ativo = true                 |
| 6     | char letra = 'a';               | PR:CHAR    | DECLARA          | ACEITA    | letra = 'a'                  |
| 7     | char vazio = '';                | PR:CHAR    | DECLARA          | ACEITA    | vazio = ''                   |
| 8     | char mensagem = "compiladores"; | PR:CHAR    | DECLARA          | ACEITA    | mensagem = "compiladores"    |
| 9     | char texto_vazio = "";          | PR:CHAR    | DECLARA          | ACEITA    | texto_vazio = ""             |
| 10    | int nome, idade=23, filhos=3;   | PR:INT     | DECLARA_MULTIPLO | ACEITA    | nome, idade = 23, filhos = 3 |
| 11    | int erro_atribuicao = ;         | PR:INT     | -                | REJEITADA | -                            |
| 12    | float = 10;                     | PR:FLOAT   | -                | REJEITADA | -                            |
| 13    | double sem_ponto_virgula        | PR:DOUBLE  | -                | REJEITADA | sem_ponto_virgula            |
+-------+---------------------------------+------------+------------------+-----------+------------------------------+
```

---

## Estrutura dos Arquivos

- [`analisador_sintatico.py`](analisador_sintatico.py): Analisador léxico e sintático com geração de árvore de derivação, tabela sintática e exportação para CSV.
- [`sintaxe.txt`](sintaxe.txt): Registro formal das produções da gramática.
- [`input.c`](input.c): Arquivo de entrada com os códigos de teste.
- [`tabela_simbolos.csv`](tabela_simbolos.csv): Tabela de símbolos gerada após a execução.
