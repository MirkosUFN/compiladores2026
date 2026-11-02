# Verificação de Tipos – Exercício 1: Memória usada para DADOS

**Aluno:** Romeo Noro Guterres

## 1. Enunciado

Utilizando um código fonte em linguagem C, verificar quantos elementos são alocados em memória, identificar seus tipos e, com base no tamanho de cada tipo, calcular quanto o trecho de código utiliza de memória para **dados**.

## 2. Código analisado

O código parte do `input.c` usado na Análise Sintática (Exercício 2), acrescido de outros tipos para cobrir `char`, `short`, `double`, `long long`, ponteiro e `struct`.

```c
#include <stdio.h>

#define TAM 3

struct Aluno {
    char   inicial;
    int    matricula;
    double media;
};

int totalAlunos = 1;

int main(void) {
    int notas[TAM] = {7, 8, 10};
    int matriz[2][2] = {{1, 2}, {3, 4}};
    float media = (notas[0] + notas[1]) / 2.0;
    char conceito = 'B';
    double pesos[2] = {0.4, 0.6};
    long long contador = 0;
    short faltas = 2;
    struct Aluno aluno = {'R', 2026, 0.0};
    int *ptr = &notas[0];
    unsigned char flags = 0;

    if (media >= 7.0) {
        if ((notas[2] > 9) && (media < 10)) {
            matriz[0][1] = 5;
        }
    } else {
        media = ((media * 2) + 1);
    }

    aluno.media = media;
    contador++;
    printf("%c %.2f %d\n", conceito, aluno.media, *ptr);

    return 0;
}
```

## 3. Tamanho de cada tipo

O padrão C não fixa o tamanho dos tipos, só o mínimo de cada um (`sizeof(char)` é sempre 1). Os valores abaixo são os usados pelo GCC em Linux x86-64 (modelo LP64), que é o ambiente mais comum. Para os tipos deste código, os tamanhos são os mesmos em Windows 64 bits.

| Tipo | Tamanho | Alinhamento | Fonte |
|---|---:|---:|---|
| `char` / `unsigned char` | 1 byte | 1 | padrão C (`sizeof(char) == 1`) |
| `short` | 2 bytes | 2 | System V ABI x86-64 |
| `int` | 4 bytes | 4 | System V ABI x86-64 |
| `float` | 4 bytes | 4 | IEEE 754 precisão simples |
| `double` | 8 bytes | 8 | IEEE 754 precisão dupla |
| `long long` | 8 bytes | 8 | System V ABI x86-64 |
| ponteiro (`int *`) | 8 bytes | 8 | endereços de 64 bits |

Referências: cppreference.com – *Arithmetic types*; System V Application Binary Interface – AMD64 Architecture Processor Supplement, seção 3.1.2 (*Data Representation*).

## 4. Elementos alocados

O código declara **11 variáveis** (1 global e 10 locais à `main`). Contando cada posição de vetor/matriz e cada campo da `struct` como um elemento, são **19 elementos** de dados.

| # | Variável | Tipo | Escopo / região | Elementos | Cálculo | Bytes |
|---:|---|---|---|---:|---|---:|
| 1 | `totalAlunos` | `int` | global (`.data`) | 1 | 1 × 4 | 4 |
| 2 | `notas` | `int[3]` | local (pilha) | 3 | 3 × 4 | 12 |
| 3 | `matriz` | `int[2][2]` | local (pilha) | 4 | 2 × 2 × 4 | 16 |
| 4 | `media` | `float` | local (pilha) | 1 | 1 × 4 | 4 |
| 5 | `conceito` | `char` | local (pilha) | 1 | 1 × 1 | 1 |
| 6 | `pesos` | `double[2]` | local (pilha) | 2 | 2 × 8 | 16 |
| 7 | `contador` | `long long` | local (pilha) | 1 | 1 × 8 | 8 |
| 8 | `faltas` | `short` | local (pilha) | 1 | 1 × 2 | 2 |
| 9 | `aluno` | `struct Aluno` | local (pilha) | 3 | ver seção 5 | 16 |
| 10 | `ptr` | `int *` | local (pilha) | 1 | 1 × 8 | 8 |
| 11 | `flags` | `unsigned char` | local (pilha) | 1 | 1 × 1 | 1 |
| | **Total** | | | **19** | | **88** |

## 5. O caso da `struct Aluno` (padding)

Somando só os campos, a struct teria 1 + 4 + 8 = 13 bytes. Mas cada campo precisa começar em um endereço múltiplo do seu alinhamento, então o compilador insere bytes de preenchimento (*padding*):

| Deslocamento | Conteúdo | Bytes |
|---:|---|---:|
| 0 | `inicial` (`char`) | 1 |
| 1–3 | padding, para `matricula` começar em múltiplo de 4 | 3 |
| 4–7 | `matricula` (`int`) | 4 |
| 8–15 | `media` (`double`) | 8 |
| | **`sizeof(struct Aluno)`** | **16** |

Se os campos fossem declarados do maior para o menor (`double`, `int`, `char`), o padding interno sumiria, mas o `sizeof` continuaria 16, porque o tamanho total é arredondado para múltiplo do maior alinhamento (8).

## 6. Resultado

| Região | Variáveis | Bytes |
|---|---|---:|
| Dados globais (`.data`) | `totalAlunos` | 4 |
| Pilha (variáveis locais de `main`) | as outras 10 | 84 |
| **Total para dados** | 11 variáveis / 19 elementos | **88 bytes** |

Sem o padding da struct, a soma "ingênua" dos tipos seria **85 bytes**. A diferença de 3 bytes mostra que o espaço de dados não é só a soma dos `sizeof` dos tipos básicos: o alinhamento também conta.

## 7. Observações

- **O que não entra no cálculo:** `TAM` é uma macro, substituída pelo pré-processador antes da compilação, e não ocupa memória. As constantes `7.0`, `10`, `2` etc. viram parte das instruções do programa. A string `"%c %.2f %d\n"` fica na área somente leitura (`.rodata`) e ocupa 12 bytes (11 caracteres + `\0`), mas é constante do programa, e não variável de dados.
- **Pilha real:** os 84 bytes são o mínimo exigido pelas variáveis locais. Na prática, o compilador pode reordenar as variáveis, inserir alinhamento entre elas e arredondar o quadro da pilha para múltiplo de 16 bytes (exigência do ABI x86-64). Com otimização (`-O2`), algumas variáveis podem ficar só em registradores e nem ocupar a pilha.
- **Como conferir:** cada valor da tabela pode ser verificado com `sizeof`, por exemplo `printf("%zu\n", sizeof(struct Aluno));`, que imprime `16`.
