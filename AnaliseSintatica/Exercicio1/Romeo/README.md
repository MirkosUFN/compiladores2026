# Exercício 1 — Análise Sintática — Romeo Noro Guterres

Nova sintaxe para declaração de variável **com inicialização**, com a gramática
completa em [sintaxe.txt](sintaxe.txt).

## Decisões da gramática

- Cada variável da lista é um **Item** que pode ter ou não inicialização, então
  `int a, b = 5, c;` é válido (mistura de variáveis inicializadas e não
  inicializadas na mesma declaração).
- O valor da inicialização **depende do tipo**:

| Tipo              | Valores aceitos                  | Exemplo                       |
|-------------------|----------------------------------|-------------------------------|
| `int`             | INTEIRO                          | `int a = 1, b;`               |
| `float`/`double`  | FRACIONARIO ou INTEIRO           | `float m = 7.5, p = 70;`      |
| `char`            | ASPAS CARACTER ASPAS             | `char c = 'R';`               |
| `boolean`         | PR:TRUE ou PR:FALSE              | `boolean ok = true;`          |
| `void`            | não aceita inicialização         | `void p;`                     |

- As listas usam recursão à direita (`ListaInt -> [VG] ItemInt ListaInt`),
  igual ao `DeclaraMultiplo` do enunciado.

## Implementação

`analisador_sintatico.py`:

1. **Léxico**: gera os tokens (`PR:INT`, `NOMEVARIAVEL`, `SATR`, `INTEIRO`,
   `FRACIONARIO`, `ASPAS`, `CARACTER`, `VG`, `PV`...) com linha e coluna, e
   grava `tabela_simbolos.csv`. Aqui os tokens **não** precisam estar separados
   por espaço (`int a=1;` funciona).
2. **Sintático**: descida recursiva, uma função por regra da gramática.
   - Declaração aceita → imprime a árvore de derivação.
   - Declaração com erro → mostra o motivo com linha/coluna e continua a
     análise (modo pânico: pula até o próximo `;` ou o próximo tipo).

## Execução

```bash
python analisador_sintatico.py           # usa input.c
python analisador_sintatico.py outro.c
```

Exemplo de saída:

```text
[OK]   linha 2: int a , b = 5 , c ;
Declara
└── DeclaraInt
    ├── PR:INT int
    ├── ItemInt
    │   └── [NOMEVARIAVEL] a
    ├── ListaInt
    │   ├── [VG] ,
    │   ├── ItemInt
    │   │   ├── [NOMEVARIAVEL] b
    │   │   ├── [SATR] =
    │   │   └── [INTEIRO] 5
    │   └── ListaInt
    │       ├── [VG] ,
    │       └── ItemInt
    │           └── [NOMEVARIAVEL] c
    └── [PV] ;

[ERRO] linha 8: int x = 3.5 ;
       valor incompatível com o tipo: esperado INTEIRO, encontrado FRACIONARIO '3.5' (linha 8, coluna 9)
```

O `input.c` traz 8 declarações válidas e 5 inválidas (tipo incompatível, char
sem aspas, falta do nome, falta de `;`, void inicializado).
