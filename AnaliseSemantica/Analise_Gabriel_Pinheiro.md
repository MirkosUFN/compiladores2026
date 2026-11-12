# Memória para DADOS em código C — Gabriel Pinheiro

## 1. Código analisado

Programa que controla o estoque e o faturamento de uma pequena lista de produtos. Ele usa variáveis globais, variáveis locais (pilha), uma matriz, um vetor de `struct` e uma área alocada dinamicamente (heap) com `malloc`.

```c
#include <stdio.h>
#include <stdlib.h>

#define QTD 3

struct Produto {
    char   codigo;
    int    estoque;
    double preco;
};

unsigned int vendas = 0;
long long    faturamento = 0;

int main(void) {
    unsigned char  categoria = 2;
    short          ano = 2026;
    float          descontos[2][3] = {{0.0f, 5.0f, 10.0f}, {2.5f, 7.5f, 15.0f}};
    long           soma_estoque = 0;
    struct Produto lista[QTD] = {{'A', 10, 4.50}, {'B', 5, 12.90}, {'C', 8, 7.25}};
    struct Produto *ptr = lista;
    int            *quantidades = malloc(QTD * sizeof(int));

    for (int i = 0; i < QTD; i++) {
        quantidades[i] = (ptr + i)->estoque;
        soma_estoque += quantidades[i];
        faturamento  += (long long)(lista[i].preco * quantidades[i]);
        vendas++;
    }

    printf("Categoria %u | Ano %d | Desconto %.1f%%\n", categoria, ano, descontos[1][2]);
    printf("Estoque %ld | Vendas %u | Faturamento %lld\n", soma_estoque, vendas, faturamento);

    free(quantidades);
    return 0;
}
```

Saída ao executar:

```
Categoria 2 | Ano 2026 | Desconto 15.0%
Estoque 23 | Vendas 3 | Faturamento 167
```

## 2. Tamanho por tipo

O padrão C ([ISO C / WG14](https://www.open-std.org/jtc1/sc22/wg14/)) só garante que `sizeof(char) == 1` e a ordem `char ≤ short ≤ int ≤ long ≤ long long`. Os tamanhos reais dependem do modelo de dados da plataforma. Foi usado o modelo **LP64** (Linux x86-64), definido no [System V AMD64 ABI, seção 3.1.2](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf) e resumido na [cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html).

| Tipo | Bytes | Observação |
|---|---:|---|
| `unsigned char` | 1 | Sempre 1 byte |
| `short` | 2 | |
| `unsigned int` | 4 | Mesmo tamanho de `int` |
| `int` | 4 | |
| `float` | 4 | Precisão simples (IEEE 754) |
| `long` | 8 | 4 bytes no Windows 64 bits (LLP64) |
| `long long` | 8 | Mínimo de 64 bits pelo padrão |
| `double` | 8 | Precisão dupla (IEEE 754) |
| ponteiro (`int *`, `struct Produto *`) | 8 | Em 64 bits |

## 3. Elementos alocados

São **10 variáveis** (2 globais + 8 locais) e **1 bloco dinâmico** no heap. Contando cada elemento de vetor/matriz e cada membro de struct, são **26 posições de dados**.

| # | Identificador | Área | Tipo | Qtde | Bytes/elem. | Total (bytes) |
|---|---|---|---|---:|---:|---:|
| 1 | `vendas` | Global (`.bss`) | `unsigned int` | 1 | 4 | 4 |
| 2 | `faturamento` | Global (`.bss`) | `long long` | 1 | 8 | 8 |
| 3 | `categoria` | Pilha | `unsigned char` | 1 | 1 | 1 |
| 4 | `ano` | Pilha | `short` | 1 | 2 | 2 |
| 5 | `descontos` | Pilha | `float[2][3]` | 6 | 4 | 24 |
| 6 | `soma_estoque` | Pilha | `long` | 1 | 8 | 8 |
| 7 | `lista` | Pilha | `struct Produto[3]` | 3 structs | 16 | 48 |
| 8 | `ptr` | Pilha | `struct Produto *` | 1 | 8 | 8 |
| 9 | `quantidades` | Pilha | `int *` | 1 | 8 | 8 |
| 10 | `i` | Pilha | `int` | 1 | 4 | 4 |
| 11 | *(bloco do `malloc`)* | Heap | `int[3]` | 3 | 4 | 12 |

> `vendas` e `faturamento` são inicializadas com zero, por isso ficam na `.bss`.
> O ponteiro `quantidades` (8 bytes, na pilha) é diferente da área para onde ele aponta (12 bytes, no heap): os dois foram contados.

### Detalhe da `struct Produto`

| Membro | Tipo | Bytes | Offset |
|---|---|---:|---|
| `codigo` | `char` | 1 | 0 |
| *(padding)* | — | 3 | 1–3 |
| `estoque` | `int` | 4 | 4–7 |
| `preco` | `double` | 8 | 8–15 |
| **Total** | | **16** | |

Os membros somam 13 bytes, mas o `int` precisa começar em endereço múltiplo de 4, então o compilador insere 3 bytes de padding depois de `codigo`. A struct fica com 16 bytes (múltiplo de 8, o alinhamento do `double`). Se `codigo` fosse declarado por último, o resultado seria o mesmo: 13 bytes + 3 de padding no final.

## 4. Cálculo

```
Globais:  4 + 8                                   =  12 bytes
Pilha:    1 + 2 + 24 + 8 + 48 + 8 + 8 + 4         = 103 bytes
Heap:     3 × 4                                   =  12 bytes
-------------------------------------------------------------
TOTAL DE DADOS                                    = 127 bytes (1016 bits)
```

**Resultado: o trecho usa 127 bytes de memória para dados.**

Desses 127 bytes, 9 são padding da struct (3 bytes × 3 produtos). Sem o padding, os dados úteis somariam 118 bytes.

### Variações

| Situação | Total |
|---|---:|
| Linux 64 bits, LP64 (referência) | **127 bytes** |
| Windows 64 bits, LLP64 (`long` = 4) | 123 bytes |
| Sem padding na struct (hipotético) | 118 bytes |

## 5. Verificação

`sizeof` e `offsetof` medidos com GCC em x86_64:

```
unsigned char 1 | short 2 | unsigned int 4 | int 4 | long 8 | long long 8
float 4 | double 8 | ponteiro 8 | float[2][3] 24
struct Produto 16 | struct Produto[3] 48
offsetof: codigo 0 | estoque 4 | preco 8
```

## 6. O que não foi contado

- Código de máquina das instruções (área de texto).
- Strings literais dos `printf` (área somente leitura, `.rodata`).
- A constante `QTD`, que é macro e some no pré-processamento.
- Cabeçalho interno que o `malloc` guarda junto ao bloco (no glibc, normalmente 8 a 16 bytes a mais).
- Endereço de retorno, frame pointer e alinhamento extra da pilha.

## Fontes

- [ISO C / WG14 — Programming Languages — C](https://www.open-std.org/jtc1/sc22/wg14/)
- [cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html)
- [System V AMD64 ABI — Data Representation (seção 3.1.2)](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf)
- [Microsoft Learn — Storage of basic types](https://learn.microsoft.com/en-us/cpp/c-language/storage-of-basic-types) (variante Windows)
