# Análise de Consumo de Memória em C

## Código Fonte em C

```c
#include <stdio.h>

int main() {
    int idade = 25;            // Elemento 1
    float altura = 1.75f;      // Elemento 2
    char inicial = 'J';        // Elemento 3
    double salario = 4500.50;  // Elemento 4
    int numeros[3] = {10, 20, 30}; // Elemento 5 (Vetor com 3 elementos inteiros)
    
    return 0;
}
```

## Identificação e Tamanho dos Elementos em Memória

| Variável | Tipo de Dados | Quantidade de Elementos | Tamanho Unitário | Memória Total Utilizada |
| :--- | :--- | :--- | :--- | :--- |
| `idade` | `int` | 1 | 4 bytes | 4 bytes |
| `altura` | `float` | 1 | 4 bytes | 4 bytes |
| `inicial` | `char` | 1 | 1 byte | 1 byte |
| `salario` | `double` | 1 | 8 bytes | 8 bytes |
| `numeros` | `int` (vetor) | 3 | 4 bytes (cada) | 12 bytes ($3 \times 4$) |

## Cálculo do Consumo Total para Dados

Somando os bytes ocupados por cada elemento declarado no escopo da função:

4 (idade) + 4 (altura) + 1 (inicial) + 8 (salario) + 12 (vetor numeros) = **29 bytes**
