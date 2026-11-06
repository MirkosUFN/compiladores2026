# Análise de Código em C e Alocação de Memória

Este documento apresenta o programa em C desenvolvido para contar vogais em uma palavra, seguido pela análise detalhada dos elementos alocados em memória e o consumo de dados.

---

## 1. Código Fonte em C

```c
#include <stdio.h>
#include <ctype.h> 

int main() {
    char palavra[100];
    int i, contador = 0;

    printf("Digite uma palavra: ");
    scanf("%s", palavra); 

    for (i = 0; palavra[i] != '\0'; i++) {

        char c = tolower(palavra[i]);

        if (c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u') {
            contador++;
        }
    }
    printf("A palavra '%s' possui %d vogais.\n", palavra, contador);

    return 0;
}
```

---

## 2. Identificação dos Elementos e Tipos

As variáveis locais declaradas na função `main` e utilizadas pelo programa são:

* **`palavra[100]`**: Um vetor (array) do tipo **`char`** composto por $100$ elementos.
* **`i`**: Uma variável do tipo **`int`** com $1$ elemento, usada como contador do loop `for`.
* **`contador`**: Uma variável do tipo **`int`** com $1$ elemento, usada para acumular o total de vogais.
* **`c`**: Uma variável do tipo **`char`** com $1$ elemento, declarada dentro do escopo do loop para armazenar o caractere convertido.

---

## 3. Tamanho Padrão dos Tipos em Memória

Considerando arquiteturas padrão de 32 e 64 bits (como GCC em x86/x86_64):
* **`char`**: Ocupa **$1$ byte** ($8$ bits).
* **`int`**: Ocupa **$4$ bytes** ($32$ bits).

---

## 4. Tabela de Cálculo de Memória para DADOS

| Variável | Tipo de Dado | Quantidade de Elementos | Tamanho Unitário | Total de Memória |
| :--- | :--- | :--- | :--- | :--- |
| **`palavra`** | `char` | $100$ | $1$ byte | $100 \times 1 = \mathbf{100\text{ bytes}}$ |
| **`i`** | `int` | $1$ | $4$ bytes | $1 \times 4 = \mathbf{4\text{ bytes}}$ |
| **`contador`** | `int` | $1$ | $4$ bytes | $1 \times 4 = \mathbf{4\text{ bytes}}$ |
| **`c`** | `char` | $1$ | $1$ byte | $1 \times 1 = \mathbf{1\text{ byte}}$ |
| **TOTAL** | — | — | — | $\mathbf{109\text{ bytes}}$ |

### Nota sobre Alinhamento de Memória (*Padding*)
O somatório bruto dos dados declarados resulta em **$109$ bytes**.
