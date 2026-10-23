# Análise de memória de um programa simples em C

## 1. Objetivo

O objetivo é identificar os dados declarados no código-fonte, consultar quanto espaço seus tipos normalmente ocupam e calcular uma estimativa da memória destinada aos dados. O programa também imprime `Hello, World!`, lê dois números inteiros e mostra a soma.

> **Importante:** não se deve somar o tamanho do texto impresso à memória das variáveis como se fossem a mesma medida. A memória dos objetos de dados e a quantidade de bytes enviados ao terminal são coisas diferentes. Além disso, o tamanho exato do programa em memória depende do compilador, da arquitetura, das otimizações e do ambiente de execução.

## 2. Código-fonte (`matheus_nogueira_analise.c`)

```c
#include <stdio.h>

int main(void)
{
    int numero1;
    int numero2;
    int resultado;

    printf("Hello, World!\n");
    printf("Digite um numero inteiro: ");
    scanf("%d", &numero1);
    printf("Digite outro numero inteiro: ");
    scanf("%d", &numero2);

    resultado = numero1 + numero2;
    printf("Soma: %d\n", resultado);

    return 0;
}
```

## 3. Como compilar e executar

No Linux ou macOS, com GCC instalado:

```bash
gcc -std=c11 -Wall -Wextra -Wpedantic matheus_nogueira_analise.c -o matheus_nogueira_analise
./matheus_nogueira_analise
```

- `gcc`: chama o compilador GCC.
- `-std=c11`: seleciona o padrão C11.
- `-Wall`: ativa um conjunto amplo de avisos.
- `-Wextra`: ativa avisos adicionais.
- `-Wpedantic`: solicita avisos sobre extensões que não seguem estritamente o padrão selecionado.
- `matheus_nogueira_analise.c`: arquivo de código-fonte.
- `-o matheus_nogueira_analise`: define o nome do executável produzido.
- `./matheus_nogueira_analise`: executa o programa no diretório atual.

## 4. Elementos de dados declarados

O programa declara **3 variáveis**, todas do tipo `int`.

| Variável | Tipo | Tamanho típico no ambiente Linux x86-64 com GCC | Cálculo |
|---|---|---:|---:|
| `numero1` | `int` | 4 bytes | 4 × 8 = 32 bits |
| `numero2` | `int` | 4 bytes | 4 × 8 = 32 bits |
| `resultado` | `int` | 4 bytes | 4 × 8 = 32 bits |
| **Total nominal** | **3 variáveis `int`** | **12 bytes** | **96 bits** |

O tamanho de `int` não é obrigatoriamente 4 bytes em todas as implementações de C. Os 12 bytes são uma estimativa típica para a plataforma indicada; o padrão C permite outros tamanhos, desde que seus requisitos mínimos sejam respeitados.

## 5. Como contar bytes de strings

Em C, uma string literal é armazenada como uma sequência de caracteres terminada pelo caractere nulo `\0`. O caractere `\n` dentro de uma string representa **um caractere de nova linha**, não dois caracteres separados. Em UTF-8, os textos deste exemplo usam caracteres ASCII, então cada caractere visível, espaço, `%`, `d` ou nova linha ocupa um byte. O terminador `\0` acrescenta mais um byte ao armazenamento de cada literal.

| Literal no código | Bytes dos caracteres (incluindo `\n`, se houver) | Terminador `\0` | Tamanho nominal da literal |
|---|---:|---:|---:|
| `"Hello, World!\n"` | 14 | 1 | 15 bytes |
| `"Digite um numero inteiro: "` | 26 | 1 | 27 bytes |
| `"%d"` (usada em `scanf`) | 2 | 1 | 3 bytes |
| `"Digite outro numero inteiro: "` | 29 | 1 | 30 bytes |
| `"%d"` (usada em `printf`) | 2 | 1 | 3 bytes |
| `"Soma: %d\n"` | 9 | 1 | 10 bytes |
| **Total contando cada ocorrência separadamente** | **82** | **6** | **88 bytes** |

O total de 88 bytes é a soma nominal das ocorrências das strings literais no código, contando cada ocorrência separadamente. O compilador pode compartilhar armazenamento de literais iguais, como as duas ocorrências de `"%d"`; por isso, não se deve afirmar que elas obrigatoriamente ocupam 88 bytes distintos na execução.

## 6. Estimativa nominal dos dados

Usando os tamanhos típicos da tabela e contando cada ocorrência de literal separadamente:

| Categoria | Estimativa |
|---|---:|
| 3 variáveis `int` | 12 bytes = 96 bits |
| Literais de string, por ocorrência | 88 bytes = 704 bits |
| **Soma nominal ilustrativa** | **100 bytes = 800 bits** |

**A soma de 100 bytes não é a memória total do processo nem uma garantia de memória simultaneamente alocada.** É uma soma didática das três variáveis e das ocorrências de strings literais, assumindo `sizeof(int) == 4` e sem deduplicação de literais. O compilador pode compartilhar literais e otimizar o código. A memória ocupada pelo executável, pelas instruções de máquina, pela biblioteca padrão, pela pilha e por estruturas de execução não está incluída.

## 7. O que conta e o que não conta como dado

- **Variáveis (`numero1`, `numero2`, `resultado`):** são objetos de dados; seus tamanhos podem ser estimados com base no tipo e na implementação.
- **Strings literais:** são objetos de armazenamento estático que incluem um terminador `\0`; literais iguais podem compartilhar armazenamento.
- **`main`, `printf`, `scanf` e `return 0`:** são elementos do código-fonte/instruções e do fluxo de execução, não variáveis adicionais. Não se soma o tamanho textual dessas palavras como se cada letra ocupasse memória de dados durante a execução.
- **`#include <stdio.h>`:** é uma diretiva de pré-processador; não significa que o texto do cabeçalho inteiro seja copiado para a memória de dados do programa. As funções da biblioteca usadas podem afetar o executável e a memória do processo, mas isso não pode ser calculado somando os caracteres da diretiva.
- **Valores digitados:** ficam armazenados nas variáveis inteiras correspondentes. O número de caracteres digitados não altera o tamanho dessas variáveis `int`, desde que o valor seja representável pelo tipo.
- **Saída no terminal:** contar os bytes impressos mede a saída produzida, não a memória total ocupada pelo programa.

## 8. Exemplo de execução

```text
Hello, World!
Digite um numero inteiro: 5
Digite outro numero inteiro: 3
Soma: 8
```

Os valores `5` e `3` são entradas do usuário. Eles não fazem parte da saída produzida pelo programa antes da digitação; terminais normalmente mostram os caracteres digitados (eco), mas isso é comportamento do terminal, não uma impressão feita por `printf`.

## 9. Referências

- ISO C / WG14, *Programming Languages — C* (padrão da linguagem): https://www.open-std.org/jtc1/sc22/wg14/
- cppreference, *Arithmetic types*: https://en.cppreference.com/w/c/language/arithmetic_types.html
- cppreference, *String literals*: https://en.cppreference.com/w/c/language/string_literal.html
- Harvard University, CS61, *Data Representation*: https://cs61.seas.harvard.edu/site/2026/Datarep/
