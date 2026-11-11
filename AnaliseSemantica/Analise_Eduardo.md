# Consumo de memória para DADOS em código C

## 1. Código-fonte analisado

```c
#include <stdio.h>

#define TAM 5

struct Aluno {
    int   matricula;
    float nota;
    char  inicial;
};

int    contador = 0;
double media    = 0.0;

int main(void) {
    char   letra = 'A';
    short  idade = 20;
    int    i;
    int    notas[TAM] = {7, 8, 6, 9, 10};
    float  preco = 9.5f;
    long   total = 0;
    struct Aluno aluno = {1, 8.5f, 'E'};
    int   *ptr = notas;

    for (i = 0; i < TAM; i++) {
        total += *(ptr + i);
        contador++;
    }
    media = (double)total / TAM;

    printf("Letra: %c | Idade: %d | Preco: %.2f\n", letra, idade, preco);
    printf("Aluno: %d %.1f %c\n", aluno.matricula, aluno.nota, aluno.inicial);
    printf("Contador: %d | Media: %.2f\n", contador, media);
    return 0;
}
```

## 2. Tamanho por tipo

O padrão C ([ISO C / WG14](https://www.open-std.org/jtc1/sc22/wg14/)) não fixa o tamanho dos tipos: garante apenas que `sizeof(char) == 1` e que `char ≤ short ≤ int ≤ long ≤ long long`. O tamanho real depende do *modelo de dados* da plataforma ([cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html)). Em Linux x86-64 vale o modelo **LP64**, e os tamanhos e alinhamentos vêm do [System V AMD64 ABI, seção 3.1.2](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf). No Windows 64 bits vale o **LLP64**.

| Tipo | Tamanho (bytes) | Observação | Fonte |
|---|---|---|---|
| `char` | 1 | Sempre 1 byte, por definição do padrão | ISO C / WG14, [cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html) |
| `short` | 2 | LP64 e LLP64 | [cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html), [System V AMD64 ABI, seção 3.1.2](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf) |
| `int` | 4 | LP64 e LLP64 | [cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html), [System V AMD64 ABI, seção 3.1.2](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf) |
| `long` | 8 (LP64) / 4 (LLP64) | Muda entre Linux 64 bits e Windows 64 bits | [cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html), [Microsoft Learn](https://learn.microsoft.com/en-us/cpp/c-language/storage-of-basic-types) |
| `float` | 4 | Precisão simples | [System V AMD64 ABI, seção 3.1.2](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf) |
| `double` | 8 | Precisão dupla | [System V AMD64 ABI, seção 3.1.2](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf) |
| ponteiro (`int *`) | 8 | Em 64 bits (LP64 e LLP64) | [cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html), [System V AMD64 ABI, seção 3.1.2](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf) |

## 3. Elementos alocados

São **10 variáveis** declaradas, que ocupam **16 posições de dados** se contarmos cada elemento do array e cada membro da struct.

| # | Identificador | Escopo / área | Tipo | Qtde de elementos | Bytes por elemento | Total (bytes) |
|---|---|---|---|---|---|---|
| 1 | `contador` | Global (área de dados) | `int` | 1 | 4 | 4 |
| 2 | `media` | Global (área de dados) | `double` | 1 | 8 | 8 |
| 3 | `letra` | Local (pilha) | `char` | 1 | 1 | 1 |
| 4 | `idade` | Local (pilha) | `short` | 1 | 2 | 2 |
| 5 | `i` | Local (pilha) | `int` | 1 | 4 | 4 |
| 6 | `notas` | Local (pilha) | `int[5]` | 5 | 4 | 20 |
| 7 | `preco` | Local (pilha) | `float` | 1 | 4 | 4 |
| 8 | `total` | Local (pilha) | `long` | 1 | 8 | 8 |
| 9 | `aluno` | Local (pilha) | `struct Aluno` | 3 membros | ver abaixo | 12 |
| 10 | `ptr` | Local (pilha) | `int *` | 1 | 8 | 8 |

### Detalhe da `struct Aluno`

| Membro | Tipo | Bytes | Offset |
|---|---|---|---|
| `matricula` | `int` | 4 | 0 |
| `nota` | `float` | 4 | 4 |
| `inicial` | `char` | 1 | 8 |
| *(padding)* | — | 3 | 9–11 |
| **Total** | | **12** | |

Os 3 bytes de padding existem porque a struct é alinhada ao maior membro (4 bytes).

## 4. Cálculo

```
Globais:  4 + 8                               = 12 bytes
Locais:   1 + 2 + 4 + 20 + 4 + 8 + 12 + 8     = 59 bytes
---------------------------------------------------------
TOTAL DE DADOS                                = 71 bytes
```

**Resultado: o trecho utiliza 71 bytes de memória para dados.**

### Variações

| Situação | Total |
|---|---|
| Linux 64 bits (referência) | **71 bytes** |
| Windows 64 bits (`long` = 4) | 67 bytes |
| Se a struct não tivesse padding (hipotético) | 68 bytes |

## 5. O que não foi contado

- Código de máquina das instruções (área de texto).
- Literais de string do `printf` (área somente leitura, `.rodata`).
- Constante `TAM`, que é macro e some no pré-processamento, sem ocupar memória.
- Endereço de retorno, frame pointer e alinhamento extra da pilha, que são controle e não dados do programa.
- Memória dinâmica: não há `malloc` neste código.

## 6. Verificação

`sizeof` medido em x86_64 com GCC:

```
char 1 | short 2 | int 4 | float 4 | long 8 | double 8 | ptr 8 | struct Aluno 12 | int[5] 20
```

## Fontes

- [ISO C / WG14 — Programming Languages — C (padrão da linguagem)](https://www.open-std.org/jtc1/sc22/wg14/)
- [cppreference — Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types.html)
- [System V AMD64 ABI — Data Representation (seção 3.1.2)](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf)
- [Microsoft Learn — Storage of basic types](https://learn.microsoft.com/en-us/cpp/c-language/storage-of-basic-types) (variante Windows)
