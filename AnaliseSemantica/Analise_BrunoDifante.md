# Verificação de tipos — Exercício 1 — Bruno Difante

Analisei o mesmo código C do meu [Exercício 2 de Análise Sintática](../AnaliseSintatica/Exerc%C3%ADcio%202/BrunoDifante/input.c).

## Código analisado

~~~c
int main(void) {
    int dados[3] = {8, 6, 10};
    double media = (dados[0] + dados[1] + dados[2]) / 3.0;
    char conceito = 'B';
    if (media >= 7.0 && conceito == 'B') {
        /* Os delimitadores neste comentário [({ são ignorados. */
        return 0;
    }
    return 1;
}
~~~

## Memória para dados

Usei os tamanhos de C no GCC para Linux x86-64 (LP64), com 8 bits por byte.
A tabela representa a soma dos tamanhos dos objetos declarados. O operador
sizeof retorna o tamanho do objeto em bytes de C. Para um vetor, o tamanho
é o número de elementos multiplicado pelo tamanho de cada elemento.

| Objeto | Tipo | Elementos escalares | Bytes por elemento | Subtotal |
|---|---|---:|---:|---:|
| dados | int[3] | 3 | 4 | 12 |
| media | double | 1 | 8 | 8 |
| conceito | char | 1 | 1 | 1 |
| **Total** | | **5** | | **21 bytes** |

Há **3 objetos declarados** e **5 elementos escalares**, contando cada
posição do vetor. O total é **12 + 8 + 1 = 21 bytes (168 bits)**. A
contagem descreve os objetos do código fonte. O espaço real do quadro de
pilha pode variar por alinhamento e otimizações do compilador. Os literais
numéricos e de caractere usados nas expressões são valores, sem objetos
adicionais declarados no trecho.

## Fontes

- [GCC — modelo de dados de -m64 em x86](https://gcc.gnu.org/onlinedocs/gcc/x86-Options.html)
- [System V AMD64 ABI — tamanhos dos tipos escalares](https://gitlab.com/x86-psABIs/x86-64-ABI)
- [cppreference — operador sizeof em C](https://en.cppreference.com/w/c/language/sizeof)
