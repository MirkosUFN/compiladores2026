# Memória para DADOS em código C

## 1. Código analisado

```c
#include <stdio.h>

int total = 0;

int main(void) {
    char   c = 'A';
    short  s = 10;
    int    v[4] = {1, 2, 3, 4};
    float  f = 2.5f;
    double d = 3.14;
    int   *p = v;

    for (int i = 0; i < 4; i++)
        total += *(p + i);

    printf("%d %c %d %.1f %.2f\n", total, c, s, f, d);
    return 0;
}
```

## 2. Tamanho por tipo

Modelo **LP64** (Linux/macOS 64 bits), conforme o [System V AMD64 ABI, seção 3.1.2](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf) e a [cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html).

| Tipo | Bytes |
|---|---:|
| `char` | 1 |
| `short` | 2 |
| `int` | 4 |
| `float` | 4 |
| `double` | 8 |
| ponteiro (`int *`) | 8 |

## 3. Elementos alocados

São **8 variáveis**, ou **11 posições de dados** se contarmos cada elemento do vetor `v`.

| # | Variável | Área | Tipo | Qtde | Bytes/elem. | Total (bytes) |
|---|---|---|---|---:|---:|---:|
| 1 | `total` | Global | `int` | 1 | 4 | 4 |
| 2 | `c` | Pilha | `char` | 1 | 1 | 1 |
| 3 | `s` | Pilha | `short` | 1 | 2 | 2 |
| 4 | `v` | Pilha | `int[4]` | 4 | 4 | 16 |
| 5 | `f` | Pilha | `float` | 1 | 4 | 4 |
| 6 | `d` | Pilha | `double` | 1 | 8 | 8 |
| 7 | `p` | Pilha | `int *` | 1 | 8 | 8 |
| 8 | `i` | Pilha | `int` | 1 | 4 | 4 |

## 4. Cálculo

```
Global:  4                               =  4 bytes
Locais:  1 + 2 + 16 + 4 + 8 + 8 + 4      = 43 bytes
----------------------------------------------------
TOTAL DE DADOS                           = 47 bytes (376 bits)
```

**Resultado: o trecho usa 47 bytes de memória para dados.**

Verificação com `sizeof` ao compilar: `char 1 | short 2 | int 4 | float 4 | double 8 | ptr 8 | int[4] 16`. A soma deu 47.

## 5. Não contado

- Código de máquina (área de texto).
- A string literal do `printf` (`.rodata`).
- Alinhamento e padding da pilha, endereço de retorno e frame pointer.

## Fontes

- [ISO C / WG14](https://www.open-std.org/jtc1/sc22/wg14/)
- [cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html)
- [System V AMD64 ABI](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf)
