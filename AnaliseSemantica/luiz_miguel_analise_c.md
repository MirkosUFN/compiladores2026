# Análise de memória de um programa simples em C

## 1. Tabela dos tipos de dados em C

Tamanhos típicos em **Linux x86-64, modelo LP64**, assumindo `CHAR_BIT == 8` (8 bits por byte):

| Tipo | Bytes | Bits |
|---|---:|---:|
| `char` | 1 | 8 |
| `short` | 2 | 16 |
| `int` | 4 | 32 |
| `long` | 8 | 64 |
| `long long` | 8 | 64 |
| `float` | 4 | 32 |
| `double` | 8 | 64 |
| `long double` | 16 | 128 |

> Esses valores dependem da implementação. Em particular, `long double` pode ter tamanho diferente em outras plataformas. `sizeof` mede o tamanho em bytes de C, e `CHAR_BIT` informa quantos bits há em cada byte.

## 2. Código C de entrada

```c
#include <stdio.h>

int main(void) {
    int idade = 20;
    float altura = 1.75f;
    char inicial = 'M';

    printf("Hello World!\n");
    printf("Idade: %d\n", idade);
    printf("Altura: %.2f\n", altura);
    printf("Inicial: %c\n", inicial);

    return 0;
}
```

O programa declara **3 variáveis** e utiliza **4 ocorrências de strings literais**. O `printf` produz saída no terminal, mas os bytes impressos não são, por si só, a medida da memória ocupada pelos dados.

## 3. Resultado da análise de memória

### 3.1 Variáveis

| Variável | Tipo | Bytes | Bits |
|---|---|---:|---:|
| `idade` | `int` | 4 | 32 |
| `altura` | `float` | 4 | 32 |
| `inicial` | `char` | 1 | 8 |
| **Total: 3 variáveis** | | **9** | **72** |

**Cálculo:** 4 + 4 + 1 = **9 bytes**, ou **72 bits**.

### 3.2 Strings literais

Cada string literal em C inclui um caractere nulo final (`\0`). O escape `\n` representa **um único caractere** de nova linha. Neste exemplo, os caracteres são ASCII, com um byte cada na plataforma adotada.

| String literal | Bytes de conteúdo (inclui `\n`) | `\0` | Total |
|---|---:|---:|---:|
| `"Hello World!\n"` | 13 | 1 | 14 |
| `"Idade: %d\n"` | 10 | 1 | 11 |
| `"Altura: %.2f\n"` | 13 | 1 | 14 |
| `"Inicial: %c\n"` | 12 | 1 | 13 |
| **Total: 4 literais** | **48** | **4** | **52** |

**Cálculo:** 14 + 11 + 14 + 13 = **52 bytes**, ou **416 bits**.

### 3.3 Total nominal dos dados

| Categoria | Bytes | Bits |
|---|---:|---:|
| 3 variáveis | 9 | 72 |
| 4 strings literais | 52 | 416 |
| **Soma nominal** | **61** | **488** |

**Cálculo:** 9 + 52 = **61 bytes**; 61 × 8 = **488 bits**.

Essa é uma **soma didática dos tamanhos dos objetos de dados**, não uma medição da memória total do processo nem uma garantia de 61 bytes distintos alocados em execução. O compilador pode otimizar ou compartilhar literais. Não foram incluídos alinhamento, instruções de máquina, bibliotecas, pilha e outras estruturas de execução.

### 3.4 Conferência com `sizeof` em C

O trecho abaixo pode ser inserido antes de `return 0;` para verificar os tamanhos no compilador utilizado:

```c
#include <limits.h> /* acrescentar no inicio do arquivo */

/* Dentro de main, antes de return 0: */
size_t bytes_variaveis = sizeof(idade) + sizeof(altura) + sizeof(inicial);
size_t bytes_literais = sizeof("Hello World!\n")
                       + sizeof("Idade: %d\n")
                       + sizeof("Altura: %.2f\n")
                       + sizeof("Inicial: %c\n");

printf("Variaveis: %zu bytes\n", bytes_variaveis);
printf("Literais: %zu bytes\n", bytes_literais);
printf("Soma nominal: %zu bytes (%zu bits)\n",
       bytes_variaveis + bytes_literais,
       (bytes_variaveis + bytes_literais) * CHAR_BIT);
```

> `sizeof("texto")` inclui o `\0`. Esse cálculo soma cada ocorrência de literal separadamente, sem afirmar que o compilador necessariamente reserva blocos distintos para todas elas.

### 3.5 O que foi contabilizado

- **Variáveis:** `idade`, `altura` e `inicial` são objetos de dados.
- **Strings literais:** os quatro textos usados nos `printf` também são objetos de dados, com terminador `\0`.
- **Não contabilizados:** `main`, `printf`, `return`, diretivas `#include`, instruções compiladas e bytes enviados ao terminal não são variáveis adicionais. As bibliotecas e estruturas de execução podem consumir memória, mas não entram nesta soma nominal.

## Referências

- [ISO C / WG14 — Padrão da linguagem C](https://www.open-std.org/jtc1/sc22/wg14/)
- [cppreference — Tipos aritméticos em C](https://en.cppreference.com/w/c/language/arithmetic_types.html)
- [cppreference — Strings literais em C](https://en.cppreference.com/w/c/language/string_literal.html)
- [System V AMD64 ABI — Convenções de tipos em x86-64](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf)
