# AUTOMATO FINITO DETERMINISCITO PARA REALIZAR ANÁLISE LÉXICA

## Executar o programa

* rodar o teste da análise:

    ``` shell
    python3 -m teste.codigo
    ```

## Grafo do automato

``` mermaid
graph
    Start([começo]) ---> q0([q0])
    q5 --> |"a-zA-Z"| q5
    q0 --> |"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q1(((q1)))
    q0 --> |"+, -"| q4([q4])
    q4 --> |"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q1
    q1 --> |"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q1
    q1 --> |"."| q2([q2])
    q4 --> |"."| q2([q2])
    q0 --> |"."| q2([q2])
    q2 --> |"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q3(((q3)))
    q3 --> |"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q3(((q3)))
    q0 --> |"a-zA-Z"| q5(((q5)))
    
    q0 --> |"="| q6(((q6)))
    q6 --> |"="| q7(((q7)))
    q0 --> |"&lt; >"| q8(((q8)))
    q8 --> |"="| q7
    q0 --> |"!"| q9([q9])
    q9 --> |"="| q7
    q0 --> |";"| q10(((q10)))
    q0 --> |","| q11(((q11)))
```

### Tipos de Dados

| Estado | Tipo             |
|:------:|:----------------:|
| q0     | Inteiro          |
| q3     | Fracionado       |
| q5     | Nome de Variável |
| q6     | Atribuição       |
| q7     | Comparativo      |
| q8     | Comparativo      |
| q10    | Ponto e Virgula  |
| q11    | Virgula          |
