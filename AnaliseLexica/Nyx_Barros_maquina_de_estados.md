**Atvidade:** fazer maquina de estado em grafo que identifique um conjunto de caracteres e valide se é um numero positivo ou negativo, ele deve ser capa de categorizar numero com ou sem sinal (+, -)

``` mermaid
graph
    %% Estado Inicial
    Start([começo]) ---> q0([q0])
    
    %% Transições
    q0 -->|"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q1(((q1)))
    q0 -->|"+, -"| q4([q4])
    q4 -->|"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q1
    
    %% Loops e Pontos Decimais
    q1 -->|"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q1
    q1 -->|"."| q2([q2])
    
    %% Parte Decimal
    q2 -->|"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q3(((q3)))
    q3 -->|"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q3
```