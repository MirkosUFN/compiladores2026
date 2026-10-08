# 📚 Exercício 1 — Análise Sintática: Declaração com Inicialização

**Autor:** Gabriel Teixeira  
**Disciplina:** Compiladores (Prof. Mirkos)  
**Projeto de Referência:** [`MirkosUFN/compiladores2026/.../Romeo`](https://github.com/MirkosUFN/compiladores2026/tree/main/AnaliseSintatica/Exercicio1/Romeo)

---

## 🎯 Objetivo

Criar uma **nova sintaxe** e um **analisador léxico/sintático em Python** para a declaração de variáveis com suporte à inicialização opcional e múltipla (mista), superando a rigidez e redundância da gramática original.

A especificação formal completa da gramática encontra-se em [sintaxe.txt](sintaxe.txt).

---

## 💡 Decisões da Gramática e Arquitetura

1. **Declaração Mista com Não-Terminal `Item`**:
   - Em vez de regras separadas e inflexíveis para "todas as variáveis inicializadas" ou "nenhuma inicializada", cada variável da lista é tratada como um `Item` que pode ou não conter o operador de atribuição `[SATR]`.
   - Exemplo aceito: `int a, b = 5, c;`.

2. **Validação de Tipos por Categoria Sintática**:
   | Tipo | Valores Aceitos na Inicialização | Exemplo |
   | :--- | :--- | :--- |
   | `int` | `[INTEIRO]` | `int idade = 20, cont;` |
   | `float` / `double` | `[FRACIONARIO]` ou `[INTEIRO]` | `float media = 7.5, peso = 70;` |
   | `char` | `[ASPAS] [CARACTER] [ASPAS]` | `char letra = 'G', inicial;` |
   | `boolean` | `PR:TRUE` ou `PR:FALSE` | `boolean ativo = true, flag = false;` |
   | `void` | Não aceita inicialização | `void ponteiro;` |

3. **Recursão à Direita**:
   - As listas de variáveis utilizam recursão à direita (`ListaX -> [VG] ItemX | [VG] ItemX ListaX`), preservando o padrão adotado na disciplina.

4. **Tratamento e Recuperação de Erros (Modo Pânico)**:
   - Quando um erro sintático é detectado, o parser exibe a mensagem detalhada com a linha e a coluna do token inválido, descartando tokens até o próximo `;` (ou início de uma nova declaração) para continuar analisando o restante do arquivo.

---

## 📂 Estrutura de Arquivos

- [analisador_sintatico.py](analisador_sintatico.py): Analisador Léxico e Sintático implementado em Python (descida recursiva).
- [sintaxe.txt](sintaxe.txt): Especificação formal da gramática em BNF.
- [input.c](input.c): Arquivo de teste contendo sentenças válidas e inválidas para validação de erros.
- [tabela_simbolos.csv](tabela_simbolos.csv): Tabela de símbolos gerada automaticamente pela análise léxica em formato CSV delimitado por ponto e vírgula.

---

## 🚀 Como Executar

Execute o analisador informando o arquivo `.c` desejado (por padrão, usa `input.c`):

```bash
python analisador_sintatico.py
```

Ou especificando outro arquivo:

```bash
python analisador_sintatico.py caminho/para/outro_arquivo.c
```

---

## 🖥️ Exemplo de Saída no Terminal

```text
============================================================
 Analisador Sintático - Compiladores (Prof. Mirkos)
 Arquivo analisado: .../input.c
============================================================

[+] Tabela de símbolos gravada com sucesso em: .../tabela_simbolos.csv
[+] Total de tokens reconhecidos: 75

Iniciando Análise Sintática...

[OK]   Linha 2: int idade = 20 ;
Declara
└── DeclaraInt
    ├── PR:INT int
    ├── ItemInt
    │   ├── [NOMEVARIAVEL] idade
    │   ├── [SATR] =
    │   └── [INTEIRO] 20
    └── [PV] ;

[OK]   Linha 3: int a , b = 5 , c ;
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

[OK]   Linha 4: float media = 7.5 , peso = 70 ;
Declara
└── DeclaraFrac
    ├── TipoFrac
    │   └── PR:FLOAT float
    ├── ItemFrac
    │   ├── [NOMEVARIAVEL] media
    │   ├── [SATR] =
    │   └── ValorFrac
    │       └── [FRACIONARIO] 7.5
    ├── ListaFrac
    │   ├── [VG] ,
    │   └── ItemFrac
    │       ├── [NOMEVARIAVEL] peso
    │       ├── [SATR] =
    │       └── ValorFrac
    │           └── [INTEIRO] 70
    └── [PV] ;

[ERRO] Linha 12: int x = 3.5 ;
       => Valor incompatível com o tipo: esperado INTEIRO, encontrado FRACIONARIO '3.5' (linha 12, coluna 9)

[ERRO] Linha 13: char nome = 10 ;
       => Variável char deve ser inicializada com caractere entre aspas simples (ex: 'a'), encontrado '10' (linha 13, coluna 13)

[ERRO] Linha 14: float = 2.0 ;
       => Esperado identificador da variável, encontrado '=' (linha 14, coluna 7)

[ERRO] Linha 15: boolean flag = true
       => Esperado ';' (ponto e vírgula), encontrado 'void' (linha 16, coluna 1)

[ERRO] Linha 16: void v = 1 ;
       => Variável do tipo void não aceita inicialização de valor (linha 16, coluna 8)

------------------------------------------------------------
Resumo da Análise:
  ✔ Declarações aceitas: 8
  ✖ Declarações com erro: 5
------------------------------------------------------------
```
