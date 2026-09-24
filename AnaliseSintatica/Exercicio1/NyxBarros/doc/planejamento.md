# PLANEJAMENTO

## Grafo do automato para linguagem C

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

    q0 --> |"("| q12(((q12)))
    q0 --> |")"| q13(((q13)))
    q0 --> |"{"| q14(((q14)))
    q0 --> |"}"| q15(((q15)))
    q0 --> |"&"| q16([q16])
    q16 --> |"&"| q17(((q17)))
    q0 --> |"|"| q18([q18])
    q18 --> |"|"| q17(((q17)))
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
| q12    | Abre Parenteses  |
| q13    | Fecha Parenteses |
| q14    | Abre Chaves      |
| q15    | Fecha Chaves     |
| q17    | Operador Lógico  |

## Diagrama de Classe

``` mermaid
classDiagram
    direction LR

    class No {
        +nome : String
        +regras_transicao : Map~String, No~
        +resultado_parada : String
        +regras_transicao_string() String
    }

    class AFD {
        +estados : List~No~
        +estado_inicial : No
        +estados_finais : List~No~
        +simbolos : List~String~
        +palavras_reservadas : List~String~
        +tabela_simbolos : List~Map~
        +montar_automato(arquivo : String) void
        +analisar_arquivo(arquivo_para_analisar : String) List~Map~
        +reconhecer_palavras_reservadas(arquivo_palavras_reservadas : String) void
        +reconhecer_linha(linha : String) List~String~
        +gerar_arquivo_csv(arquivo_final : String = "teste/tabela_de_simbolos.csv") void
        +gerar_arquivo_json(arquivo_final : String = "teste/tabela_de_simbolos.json") void
        +gerar_arquivo_md(arquivo_final : String = "teste/tabela_de_simbolos.md") void
    }

    %% Composição: os estados pertencem ao AFD
    AFD "1" *-- "1..*" No : -estados

    %% Associação: referência ao estado inicial
    AFD "1" --> "1" No : -estado_inicial

    %% Associação: referência aos estados finais
    AFD "1" --> "0..*" No : -estados_finais

    %% Auto-associação: transições entre estados
    No "1" --> "0..*" No : -regras_transicao
```

## Sistema de Arquivos

    .
    ├── analizador_linguagem
    │   ├── afd.py
    │   ├── __init__.py
    │   └── no.py
    ├── config_c
    │   ├── configAfd.txt
    │   ├── palavrasReservadas.txt
    │   └── sintaxe.txt
    ├── doc
    │   ├── como usar para outras linguagens.md
    │   └── readme.md
    └── teste
        ├── codigo.py
        ├── __init__.py
        ├── tabela_de_simbolos.csv
        ├── tabela_de_simbolos.json
        ├── tabela_de_simbolos.md
        └── teste.txt

| Caminho | Descrição |
|-|-|
| `analizador_linguagem` | é onde contem o código fonte, que permite criar um automato para qualquer linguagem a partir da definião correta dos arquivos de configuração |
| `config_c/` | Pasta que contem todas as configurações para criar um automato para linguagem C |
| `config_c/configAfd.txt` | Arquivo para a configuração basica do automato |
| `config_c/palavrasReservadas.txt` | Arquivo contendo listagem completa de palavras reservadas da linguagem |
| `config_c/palavrasReservadas.txt` | Arquivo contendo todas as regras de sintaxe da linguagem |
| `doc/` | Documentação |
