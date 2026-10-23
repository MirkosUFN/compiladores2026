# Análise de Memória em C

## 1. Tabela dos tipos de dados

Tamanhos típicos em uma plataforma **64 bits (modelo LP64)**, considerando **8 bits por byte**:

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

> Os tamanhos podem variar conforme a plataforma e o compilador, especialmente `long double`.

## 2. Código C de entrada

```c
#include <stdio.h>

int main() {
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

## 3. Resultado da análise de memória

| Variável | Tipo | Bytes | Bits |
|---|---|---:|---:|
| `idade` | `int` | 4 | 32 |
| `altura` | `float` | 4 | 32 |
| `inicial` | `char` | 1 | 8 |
| **Total (3 variáveis)** | | **9** | **72** |

**Cálculo:** 4 + 4 + 1 = **9 bytes**; 9 × 8 = **72 bits**.

Para verificar os tamanhos no próprio C, adicione antes de `return 0;`:

```c
size_t total = sizeof(idade) + sizeof(altura) + sizeof(inicial);
printf("Total de variaveis: 3\n");
printf("Memoria em bytes: %zu\n", total);
printf("Memoria em bits: %zu\n", total * 8);
```

**Importante:** 9 bytes representam apenas a soma dos tamanhos das variáveis, não o consumo total de memória do programa em execução. A conversão por 8 pressupõe `CHAR_BIT == 8`.

**Referências:** [cppreference — Tipos aritméticos em C](https://en.cppreference.com/w/c/language/arithmetic_types) · [System V AMD64 ABI](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf).
