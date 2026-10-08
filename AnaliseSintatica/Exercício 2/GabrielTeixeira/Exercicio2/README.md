# 📚 Exercício 2 — Análise Sintática: Balanceamento de ( ), { } e [ ]

**Autor:** Gabriel Teixeira  
**Disciplina:** Compiladores (Prof. Mirkos)  

---

## 📌 Enunciado

> Os tokens `( )`, `{ }` e `[ ]` (abre e fecha) devem possuir contagem idêntica, ou seja, o mesmo número de abre chaves deve ser o fecha chaves.  
> O número de abre parênteses deve ser igual ao número de fecha parênteses e assim com colchetes também.  
>  
> Na tabela de símbolos, cada fecha (chaves, colchete ou parênteses) deve indicar a qual token de abrir respectivo ele se referencia, em uma coluna chamada **Ref**.

---

## 💡 Modelagem Teórica e Solução

### 1. Gramática Livre de Contexto (GLC)
A correspondência e aninhamento correto de delimitadores é a linguagem clássica de parênteses bem formados (Linguagem de Dyck), reconhecida por um **Autômato com Pilha** (Pushdown Automaton - PDA):

```bnf
# Tokens dos delimitadores
[AP]  -> (        [FP]  -> )
[ACH] -> {        [FCH] -> }
[ACO] -> [        [FCO] -> ]

# Produções sintáticas para blocos aninhados
Sequencia -> Elemento Sequencia | ε
Elemento  -> Grupo | [OUTRO]
Grupo     -> [AP]  Sequencia [FP]
           | [ACH] Sequencia [FCH]
           | [ACO] Sequencia [FCO]
```

### 2. Funcionamento do Algoritmo com Pilha
1. **Tokens de Abertura (`(`, `{`, `[`):**
   - São empilhados contendo seu `ID`, tipo, lexema, linha e coluna.
2. **Tokens de Fechamento (`)`, `}`, `]`):**
   - Se a pilha estiver vazia: acusa erro de fechamento sem abertura prévia.
   - Se o topo da pilha for a abertura correspondente:
     - O topo é desempilhado;
     - O token de fechamento recebe no atributo **`Ref`** o `ID` da abertura desempilhada.
   - Se o topo da pilha for de outro tipo: acusa erro de aninhamento incorreto / cruzamento de delimitadores (ex.: `( ... ]`).
3. **Fim do Fluxo:**
   - Se restarem tokens na pilha, cada um deles é reportado como erro (aberto e nunca fechado).
4. **Contagem:**
   - Realiza a contagem de frequência de cada símbolo para validar a regra de contagem estritamente idêntica.

---

## 📂 Arquivos do Exercício

- [analisador_sintatico.py](analisador_sintatico.py): Analisador léxico e sintático em Python com verificação de pilha e contagem de delimitadores.
- [sintaxe.txt](sintaxe.txt): Especificação formal das regras da gramática.
- [input.c](input.c): Arquivo de teste contendo código C válido (vetores, matrizes, expressões aninhadas e blocos if/else).
- [input_erros.c](input_erros.c): Arquivo de teste com erros propositais (desbalanceamento, fechamento sem abertura, cruzamento de blocos).
- [tabela_simbolos.csv](tabela_simbolos.csv): Tabela de símbolos gerada a partir do `input.c`, contendo a coluna `Ref`.
- [tabela_simbolos_input_erros.csv](tabela_simbolos_input_erros.csv): Tabela gerada para o caso de erros.

---

## 🚀 Como Executar

### 1. Teste com código válido (`input.c`):
```bash
python analisador_sintatico.py input.c
```

### 2. Teste com código inválido (`input_erros.c`):
```bash
python analisador_sintatico.py input_erros.c
```

---

## 🖥️ Exemplo de Saída no Terminal

### Execução com `input.c` (Válido):
```text
=================================================================
 Analisador Sintático - Exercício 2: Balanceamento e Referência
 Arquivo analisado: input.c
=================================================================

[+] Total de tokens reconhecidos: 106

--- DELIMITADORES IDENTIFICADOS E REFERÊNCIAS ---
  ID  Token    Tipo     Linha Coluna  Ref (ID de Abertura)
-------------------------------------------------------
   3  [        ACO          1     10  -                   
   5  ]        FCO          1     12  3                   
   7  {        ACH          1     16  -                   
  13  }        FCH          1     25  7                   
  17  [        ACO          2     11  -                   
  19  ]        FCO          2     13  17                  
  20  [        ACO          2     14  -                   
  22  ]        FCO          2     16  20                  
  24  {        ACH          2     20  -                   
  25  {        ACH          2     21  -                   
  29  }        FCH          2     26  25                  
  31  {        ACH          2     29  -                   
  35  }        FCH          2     34  31                  
  36  }        FCH          2     35  24                  
  41  (        AP           3     15  -                   
  43  [        ACO          3     21  -                   
  45  ]        FCO          3     23  43                  
  48  [        ACO          3     32  -                   
  50  ]        FCO          3     34  48                  
  51  )        FP           3     35  41                  
  ...

--- CONTAGEM DE DELIMITADORES ---
Delimitador         Aberturas  Fechamentos  Status    
-------------------------------------------------------
Parênteses ( )              7            7  OK (Igual)
Chaves { }                  7            7  OK (Igual)
Colchetes [ ]               8            8  OK (Igual)

--- RESULTADO DA ANÁLISE SINTÁTICA ---
[SUCESSO] Todos os delimitadores ( ), { } e [ ] possuem contagem idêntica,
          estão aninhados corretamente e tiveram suas referências vinculadas!

[+] Tabela de símbolos exportada em: .../tabela_simbolos.csv
=================================================================
```

---

## 📊 Estrutura da Tabela de Símbolos (`tabela_simbolos.csv`)

| ID | Token | Tipo | Linha | Coluna | Ref |
| :- | :---: | :--- | :---: | :---: | :---: |
| 1 | `int` | `PR:INT` | 1 | 1 | |
| 2 | `notas` | `NOMEVARIAVEL` | 1 | 5 | |
| **3** | `[` | `ACO` | 1 | 10 | |
| 4 | `3` | `INTEIRO` | 1 | 11 | |
| **5** | `]` | `FCO` | 1 | 12 | **3** |
| 6 | `=` | `SATR` | 1 | 14 | |
| **7** | `{` | `ACH` | 1 | 16 | |
| 8 | `7` | `INTEIRO` | 1 | 17 | |
| ... | ... | ... | ... | ... | ... |
| **13** | `}` | `FCH` | 1 | 25 | **7** |
| 14 | `;` | `PV` | 1 | 26 | |

Observe que o token `]` (ID 5) aponta para o token `[` (ID 3), e a chave `}` (ID 13) aponta para a chave `{` (ID 7).
