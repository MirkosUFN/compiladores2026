# Análise Semântica e Alocação de Memória em C

## 1. Código-Fonte em C

```c
#include <stdio.h>

int contadorGlobal = 10;
double taxaJuros = 0.05;
char statusInicial;

int main() {
    int i, j;
    float salario = 3500.50f;
    char codigo[10];
    double matriz[2][3];
    int *ptrContador = &contadorGlobal;

    for (i = 0; i < 2; i++) {
        for (j = 0; j < 3; j++) {
            matriz[i][j] = (i + j) * taxaJuros;
        }
    }

    return 0;
}
```

## 2. Tamanho dos Tipos em C (Arquitetura 64 bits)

| Tipo em C | Tamanho Padrão (Bytes) | Tamanho em Bits | 
| ----- | ----- | ----- | 
| `char` | $1\text{ byte}$ | $8\text{ bits}$ | 
| `short` | $2\text{ bytes}$ | $16\text{ bits}$ | 
| `int` | $4\text{ bytes}$ | $32\text{ bits}$ | 
| `float` | $4\text{ bytes}$ | $32\text{ bits}$ | 
| `double` | $8\text{ bytes}$ | $64\text{ bits}$ | 
| `long` | $8\text{ bytes}$ | $64\text{ bits}$ | 
| `long long` | $8\text{ bytes}$ | $64\text{ bits}$ | 
| Ponteiros (`int*`, `char*`, etc.) | $8\text{ bytes}$ | $64\text{ bits}$ | 

## 3. Tabela de Símbolos

| Identificador | Categoria | Tipo Base | Qtd. Elementos | Tamanho Unitário | Consumo Total | 
| ----- | ----- | ----- | ----- | ----- | ----- | 
| `contadorGlobal` | Variável | `int` | $1$ | $4\text{ bytes}$ | $4\text{ bytes}$ | 
| `taxaJuros` | Variável | `double` | $1$ | $8\text{ bytes}$ | $8\text{ bytes}$ | 
| `statusInicial` | Variável | `char` | $1$ | $1\text{ byte}$ | $1\text{ byte}$ | 
| `i` | Variável | `int` | $1$ | $4\text{ bytes}$ | $4\text{ bytes}$ | 
| `j` | Variável | `int` | $1$ | $4\text{ bytes}$ | $4\text{ bytes}$ | 
| `salario` | Variável | `float` | $1$ | $4\text{ bytes}$ | $4\text{ bytes}$ | 
| `codigo` | Vetor (1D) | `char` | $10$ | $1\text{ byte}$ | $10\text{ bytes}$ | 
| `matriz` | Matriz (2D) | `double` | $6$ | $8\text{ bytes}$ | $48\text{ bytes}$ | 
| `ptrContador` | Ponteiro | `int*` | $1$ | $8\text{ bytes}$ | $8\text{ bytes}$ | 

## 4. Memória Total de Dados

* **Total de Elementos Alocados:** $23\text{ elementos}$ ($9\text{ identificadores}$)

* **Memória Total de Dados:** $91\text{ bytes}$ ($728\text{ bits}$)