# AUTOMATO FINITO DETERMINISCITO PARA REALIZAR ANÁLISE LÉXICA

## Executar o programa

* rodar o teste da análise:

    ``` shell
    python3 -m teste.codigo_meu
    ```

## Grafo do automato

``` mermaid
graph
    Start([começo]) ---> q0([q0])
    q0 -->|"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q1(((q1)))
    q0 -->|"+, -"| q4([q4])
    q4 -->|"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q1
    q1 -->|"."| q2([q2])
    q1 -->|"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q1
    q4 -->|"."| q2([q2])
    q0 -->|"."| q2([q2])
    q2 -->|"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q3(((q3)))
    q3 -->|"1, 2, 3, 4, 5, 6, 7, 8, 9, 0"| q3(((q3)))
```
