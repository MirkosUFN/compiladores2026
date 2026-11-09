# Análise de memória de um programa simples em C

## 1. Objetivo

Identificar os elementos de dados declarados ou utilizados em um programa em C, seus tipos e tamanhos, e calcular uma estimativa da memória destinada aos dados.

## 2. Tabela dos tipos de dados em C

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

> Esses tamanhos dependem da implementação. `sizeof` mede o tamanho em bytes de C, e `CHAR_BIT` indica quantos bits há em cada byte. O tamanho de `long double`, em particular, pode variar entre plataformas.

## 3. Código analisado

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

O código possui **3 variáveis locais** e **4 ocorrências de strings literais**, totalizando **7 elementos de dados identificados no código-fonte**. Os bytes enviados ao terminal por `printf` não representam, por si só, a memória ocupada pelos dados do programa.

## 4. Análise da memória para dados

### 4.1. Variáveis locais (pilha / *stack*)

| Variável | Tipo | Bytes | Bits |
|---|---|---:|---:|
| `idade` | `int` | 4 | 32 |
| `altura` | `float` | 4 | 32 |
| `inicial` | `char` | 1 | 8 |
| **Total: 3 variáveis** | | **9** | **72** |

**Cálculo:** 4 + 4 + 1 = **9 bytes**, ou **72 bits**.

### 4.2. Strings literais (normalmente em `.rodata`)

Cada string literal inclui um terminador nulo (`\0`), e o escape `\n` representa **um único caractere** de nova linha. Considerando a codificação usual de um byte por caractere neste exemplo:

| String literal | Conteúdo (inclui `\n`) | Terminador `\0` | Total |
|---|---:|---:|---:|
| `"Hello World!\n"` | 13 | 1 | 14 |
| `"Idade: %d\n"` | 10 | 1 | 11 |
| `"Altura: %.2f\n"` | 13 | 1 | 14 |
| `"Inicial: %c\n"` | 12 | 1 | 13 |
| **Total: 4 strings** | **48** | **4** | **52** |

**Cálculo:** 14 + 11 + 14 + 13 = **52 bytes**, ou **416 bits**.

### 4.3. Resultado geral

| Região / categoria | Elementos | Bytes | Bits |
|---|---:|---:|---:|
| Pilha — variáveis locais | 3 | 9 | 72 |
| Dados somente leitura — strings literais | 4 | 52 | 416 |
| **Total nominal** | **7** | **61** | **488** |

**Cálculo:** 9 + 52 = **61 bytes**; 61 × 8 = **488 bits**.

Assim, o programa tem **9 bytes de variáveis declaradas** e uma **soma nominal de 61 bytes ao incluir as strings literais**.

> O total de 61 bytes é uma soma didática dos tamanhos dos objetos identificados, **não** uma medição da memória efetivamente consumida pelo processo. O compilador pode otimizar ou compartilhar literais e variáveis. Além disso, o alinhamento pode aumentar o espaço reservado na pilha.

### 4.4. Conferência com `sizeof`

Para verificar os tamanhos usando o compilador, acrescente `#include <limits.h>` no início do arquivo e insira o seguinte trecho dentro de `main`, antes de `return 0;`:

```c
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

O operador `sizeof` inclui o `\0` no tamanho de cada string literal. Essa conferência calcula os tamanhos nominais dos objetos, mas não determina o tamanho total do processo em execução.

### 4.5. O que não foi contabilizado

Não entram nessa soma as instruções de máquina, o código de `main` e `printf`, as bibliotecas, os dados internos do ambiente de execução nem os bytes impressos no terminal. Diretivas `#include` e a instrução `return` também não são variáveis a serem somadas. Eventuais bytes extras de alinhamento não foram calculados.

## 5. Conclusão

O código analisado contém **3 variáveis locais** (`idade`, `altura` e `inicial`), que somam **9 bytes**, e **4 strings literais**, que somam **52 bytes**. Portanto, a **soma nominal dos dados é de 61 bytes (488 bits)**, considerando os tamanhos adotados. Esse resultado é uma estimativa dos objetos de dados identificados, e não o consumo total de memória do programa.

## Referências

- [ISO C / WG14 — Padrão da linguagem C](https://www.open-std.org/jtc1/sc22/wg14/)
- [cppreference — Tipos aritméticos em C](https://en.cppreference.com/w/c/language/arithmetic_types.html)
- [cppreference — Strings literais em C](https://en.cppreference.com/w/c/language/string_literal.html)
- [System V AMD64 ABI — Convenções de tipos em x86-64](https://refspecs.linuxbase.org/elf/x86_64-abi-0.99.pdf)
