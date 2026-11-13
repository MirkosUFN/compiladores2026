# Análise de Alocação de Memória para Dados em C

Este documento apresenta um código-fonte simples em linguagem C para verificar quantos elementos são alocados em memória, identificar seus tipos de dados e calcular o consumo total de memória para **DADOS** (em bytes e em bits).

---

## 1. Consumo de Memória por Tipo de Dado (Referência)

De acordo com a especificação padrão de compiladores modernos em arquiteturas de 32 e 64 bits (como o GCC):

* **`char`:** $1\text{ byte} = 8\text{ bits}$ *(cada letra, número, espaço ou símbolo dentro de aspas consome $1\text{ char}$)*.
* **`int`:** $4\text{ bytes} = 32\text{ bits}$.
* **`float`:** $4\text{ bytes} = 32\text{ bits}$.
* **`double`:** $8\text{ bytes} = 64\text{ bits}$.

---

## 2. Código-Fonte Analisado (`calculo_memoria.c`)

```c
#include <stdio.h>

int main(void) {
    int idade = 25;
    float altura = 1.75;
    char letra = 'G';

    printf("ola mundo");
    printf("Letra: %c Idade: %d Altura: %f", letra, idade, altura);

    return 0;
}
```

---

## 3. Identificação e Contagem dos Elementos Alocados

### A. Função e Variáveis Declaradas ($4$ elementos)
1. **`int main`** (retorno inteiro da função principal / `return 0`):
   * **Tipo:** `int`
   * **Consumo:** $1 \times 4\text{ bytes} = 32\text{ bits}$
2. **`int idade = 25;`** (variável inteira inicializada com `25`):
   * **Tipo:** `int`
   * **Consumo:** $1 \times 4\text{ bytes} = 32\text{ bits}$
3. **`float altura = 1.75;`** (variável de ponto flutuante inicializada com `1.75`):
   * **Tipo:** `float`
   * **Consumo:** $1 \times 4\text{ bytes} = 32\text{ bits}$
4. **`char letra = 'G';`** (variável de caractere inicializada com `'G'`):
   * **Tipo:** `char`
   * **Consumo:** $1 \times 1\text{ byte} = 8\text{ bits}$

### B. Textos dentro dos `printf` ($39$ elementos do tipo `char`)
Cada caractere dentro das aspas (incluindo letras, espaços, dois-pontos e especificadores como `%d`) ocupa $1\text{ char}$ ($8\text{ bits}$):

1. **1º `printf`: `"ola mundo"`**
   * Contagem caractere a caractere: `o`(1), `l`(2), `a`(3), `[espaço]`(4), `m`(5), `u`(6), `n`(7), `d`(8), `o`(9).
   * **Quantidade:** $9\text{ elementos}$ do tipo `char`
   * **Consumo:** $9 \times 8\text{ bits} = 72\text{ bits}$ ($9\text{ bytes}$)

2. **2º `printf`: `"Letra: %c Idade: %d Altura: %f"`**
   * `"Letra: "` $\rightarrow 5\text{ letras} + 1\text{ dois-pontos} + 1\text{ espaço} = 7\text{ chars}$
   * `"%c "` $\rightarrow 1\text{ símbolo } \% + 1\text{ letra } c + 1\text{ espaço} = 3\text{ chars}$
   * `"Idade: "` $\rightarrow 5\text{ letras} + 1\text{ dois-pontos} + 1\text{ espaço} = 7\text{ chars}$
   * `"%d "` $\rightarrow 1\text{ símbolo } \% + 1\text{ letra } d + 1\text{ espaço} = 3\text{ chars}$
   * `"Altura: "` $\rightarrow 6\text{ letras} + 1\text{ dois-pontos} + 1\text{ espaço} = 8\text{ chars}$
   * `"%f"` $\rightarrow 1\text{ símbolo } \% + 1\text{ letra } f = 2\text{ chars}$
   * **Quantidade:** $7 + 3 + 7 + 3 + 8 + 2 = 30\text{ elementos}$ do tipo `char`
   * **Consumo:** $30 \times 8\text{ bits} = 240\text{ bits}$ ($30\text{ bytes}$)

---

## 4. Tabela Resumo do Cálculo de Memória para Dados

| Elemento no Código | Tipo de Dado | Quantidade | Tamanho Unitário (Bits) | Total (Bytes) | Total (Bits) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| Retorno de `int main` | `int` | $1$ | $32\text{ bits}$ | $4\text{ bytes}$ | $32\text{ bits}$ |
| Variável `idade` (`25`) | `int` | $1$ | $32\text{ bits}$ | $4\text{ bytes}$ | $32\text{ bits}$ |
| Variável `altura` (`1.75`) | `float` | $1$ | $32\text{ bits}$ | $4\text{ bytes}$ | $32\text{ bits}$ |
| Variável `letra` (`'G'`) | `char` | $1$ | $8\text{ bits}$ | $1\text{ byte}$ | $8\text{ bits}$ |
| Texto `"ola mundo"` | `char` | $9$ | $8\text{ bits}$ | $9\text{ bytes}$ | $72\text{ bits}$ |
| Texto `"Letra: %c Idade: %d Altura: %f"` | `char` | $30$ | $8\text{ bits}$ | $30\text{ bytes}$ | $240\text{ bits}$ |
| **TOTAL GERAL** | **—** | **$43\text{ elementos}$** | **—** | **$52\text{ bytes}$** | **$416\text{ bits}$** |

---

## 5. Conclusão

* **Total de elementos do tipo `int`:** $2\text{ elementos}$ ($64\text{ bits}$)
* **Total de elementos do tipo `float`:** $1\text{ elemento}$ ($32\text{ bits}$)
* **Total de elementos do tipo `char`:** $40\text{ elementos}$ ($320\text{ bits}$, sendo $1$ variável `char` e $39$ caracteres nos `printf`)
* **Memória total utilizada para DADOS:** **$52\text{ bytes}$** ou **$416\text{ bits}$**.
