# Trabalho de Compiladores: Declaração e Inicialização de Variáveis

Este projeto implementa um **Analisador Léxico e Sintático** para reconhecimento e validação de declarações de variáveis com suporte a inicialização, baseado em uma nova gramática unificada e otimizada.

---

## 1. Nova Sintaxe Proposta (BNF)

A gramática foi reformulada para eliminar a duplicação de regras presente na sintaxe original, permitindo a mistura flexível de variáveis com e sem inicialização na mesma linha:

```bnf
[TIPO]            -> PR:INT | PR:CHAR | PR:FLOAT | PR:DOUBLE | PR:VOID | PR:BOOLEAN
[VALOR]           -> INTEIRO | FRACIONARIO | CARACTER | NOMEVARIAVEL | PR:TRUE | PR:FALSE
[INICIALIZADOR]   -> ATRIBUICAO [VALOR]
[ITEM_DECLARADO]  -> NOMEVARIAVEL | NOMEVARIAVEL [INICIALIZADOR]

Declara           -> [TIPO] [ITEM_DECLARADO] [PV] 
                   | [TIPO] [ITEM_DECLARADO] DeclaraMultiplo [PV]
DeclaraMultiplo   -> [VG] [ITEM_DECLARADO] 
                   | [VG] [ITEM_DECLARADO] DeclaraMultiplo
```

---

## 2. Estrutura dos Arquivos

- **`analisador.py`**: Código-fonte do analisador léxico e sintático em Python.
- **`input.c`**: Arquivo de teste contendo casos de declaração simples, múltipla e tipos variados.
- **`tabela_simbolos.csv`**: Tabela de símbolos léxicos gerada no formato `ID;token;tipo;linha;coluna`.
- **`gramatica.txt`**: Documento teórico com a definição formal da gramática e derivações.

---

## 3. Como Executar

No terminal PowerShell ou Prompt de Comando, na pasta do projeto:

```powershell
py analisador.py
```

O programa executará:
1. Leitura do arquivo `input.c`.
2. Tokenização léxica com validação de colunas e linhas.
3. Análise sintática descendente de cada linha.
4. Exibição do relatório no console.
5. Exportação da tabela de símbolos para `tabela_simbolos.csv`.
