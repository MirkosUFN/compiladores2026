# Verificação de Tipos – Exercício 1: Memória usada para DADOS

**Aluno:** Gilberto Morales

## 1. Enunciado

> Utilizando um código fonte em linguagem C, verifique quantos elementos são alocados em memória. Identifique seus tipos e de acordo com a informação (coletada na Internet) sobre quanto cada tipo consome de memória, calcule quanto o trecho de código utiliza de memória para DADOS.

## 2. Código analisado

O programa calcula a média das notas de uma turma de 5 alunos, conta quantos tiraram 7 ou mais e define a situação da turma.

```c
#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define TOTAL_ALUNOS 5

int main(void) {
    char turma = 'B';
    int quantidade = TOTAL_ALUNOS;
    int i;
    int aprovados = 0;
    float notas[TOTAL_ALUNOS] = {7.5f, 5.0f, 8.25f, 9.0f, 6.0f};
    float soma = 0.0f;
    double media;
    char situacao[10];
    int *ptr_aprovados = &aprovados;
    bool turma_aprovada;

    for (i = 0; i < quantidade; i++) {
        soma = soma + notas[i];
        if (notas[i] >= 7.0f) {
            (*ptr_aprovados)++;
        }
    }

    media = soma / quantidade;
    turma_aprovada = media >= 7.0;

    if (turma_aprovada) {
        strcpy(situacao, "APROVADA");
    } else {
        strcpy(situacao, "EXAME");
    }

    printf("Turma %c: media %.2f, %d aprovados, situacao %s\n",
           turma, media, aprovados, situacao);
    return 0;
}
```

Saída do programa:

```
Turma B: media 7.15, 3 aprovados, situacao APROVADA
```

## 3. Quanto cada tipo ocupa

O padrão da linguagem C define apenas **tamanhos mínimos** para os tipos. O tamanho real depende da arquitetura e do compilador. Os valores abaixo são os usados em sistemas de 64 bits (modelo LP64: Linux, macOS, e também Windows 64 bits para estes tipos).

| Tipo | Tamanho | Observação |
|---|---|---|
| `char` | 1 byte | sempre 1 byte, por definição do padrão |
| `bool` (`<stdbool.h>`) | 1 byte | armazena 0 ou 1 |
| `int` | 4 bytes | inteiro de 32 bits |
| `float` | 4 bytes | ponto flutuante de precisão simples (IEEE 754) |
| `double` | 8 bytes | ponto flutuante de precisão dupla (IEEE 754) |
| ponteiro (`int *`) | 8 bytes | endereço de 64 bits |

Fontes: [cppreference – Arithmetic types](https://en.cppreference.com/w/c/language/arithmetic_types), [GeeksforGeeks – Data Types in C](https://www.geeksforgeeks.org/c/data-types-in-c/).

Os valores foram **conferidos com `sizeof`** compilando com o Apple clang 17 em arm64 (64 bits):

```
char=1 int=4 float=4 double=8 bool=1 ptr=8 float5=20 char10=10
```

## 4. Elementos alocados em memória

| # | Variável | Tipo | Qtd. de elementos | Cálculo | Bytes |
|---|---|---|---|---|---|
| 1 | `turma` | `char` | 1 | 1 × 1 | 1 |
| 2 | `quantidade` | `int` | 1 | 1 × 4 | 4 |
| 3 | `i` | `int` | 1 | 1 × 4 | 4 |
| 4 | `aprovados` | `int` | 1 | 1 × 4 | 4 |
| 5 | `notas` | `float[5]` | 5 | 5 × 4 | 20 |
| 6 | `soma` | `float` | 1 | 1 × 4 | 4 |
| 7 | `media` | `double` | 1 | 1 × 8 | 8 |
| 8 | `situacao` | `char[10]` | 10 | 10 × 1 | 10 |
| 9 | `ptr_aprovados` | `int *` | 1 | 1 × 8 | 8 |
| 10 | `turma_aprovada` | `bool` | 1 | 1 × 1 | 1 |
| | **Total** | | **23 elementos** | | **64 bytes** |

**10 variáveis** estão alocadas em memória. Contando cada posição dos vetores como um elemento separado (5 de `notas` e 10 de `situacao`), são **23 elementos**.

### Resumo por tipo

| Tipo | Elementos | Bytes |
|---|---|---|
| `char` | 11 (`turma` + 10 de `situacao`) | 11 |
| `int` | 3 | 12 |
| `float` | 6 (`soma` + 5 de `notas`) | 24 |
| `double` | 1 | 8 |
| `int *` | 1 | 8 |
| `bool` | 1 | 1 |
| **Total** | **23** | **64 bytes = 512 bits** |

## 5. Resultado

**O código usa 64 bytes (512 bits) de memória para dados** nas variáveis declaradas.

## 6. Observações

- **`TOTAL_ALUNOS` não ocupa memória:** é uma macro (`#define`). O pré-processador troca o nome pelo valor `5` antes da compilação, então não existe variável para ela.
- **Os literais de texto não entram no total acima** porque não são variáveis. Ficam na área de dados constantes (somente leitura) do programa, e cada um ocupa o número de caracteres + 1 byte do `'\0'`:
  - `"APROVADA"` → 9 bytes
  - `"EXAME"` → 6 bytes
  - a string de formato do `printf` → 49 bytes

  Somando esses literais (64 bytes), o programa usaria 128 bytes de dados no total.
- **Alinhamento:** as variáveis locais ficam na pilha (*stack*) da função `main`. O compilador pode inserir bytes de preenchimento (*padding*) para alinhar `int`, `double` e o ponteiro aos seus endereços naturais. Assim, o espaço real reservado na pilha pode ser um pouco maior que 64 bytes, e isso varia de compilador para compilador. Os 64 bytes são o espaço ocupado pelos dados em si.
- **O ponteiro e a variável apontada são separados:** `ptr_aprovados` ocupa 8 bytes para guardar o **endereço** de `aprovados`. A memória de `aprovados` (4 bytes) já foi contada na linha dela.
- **Em sistemas de 32 bits**, o ponteiro ocuparia 4 bytes, e o total cairia para 60 bytes.
