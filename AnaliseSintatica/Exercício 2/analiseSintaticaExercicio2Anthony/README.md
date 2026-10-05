# Trabalho de Compiladores: Análise Sintática - Exercício 2
## Balanceamento e Referenciação de Delimitadores `( )`, `{ }` e `[ ]`

Este projeto implementa um **Analisador Léxico e Sintático com Autômato com Pilha** para verificação de contagem idêntica e aninhamento estrutural dos delimitadores em código-fonte C, com preenchimento da coluna relacional **`Ref`** na tabela de símbolos.

---

## 1. Proposta Desenvolvida

Conforme o enunciado do Exercício 2:

1. **Contagem Idêntica:**
   - O número de abre parênteses `(` deve ser igual ao número de fecha parênteses `)`.
   - O número de abre chaves `{` deve ser igual ao número de fecha chaves `}`.
   - O número de abre colchetes `[` deve ser igual ao número de fecha colchetes `]`.

2. **Coluna `Ref` na Tabela de Símbolos:**
   - Na tabela de símbolos gerada em CSV (`tabela_simbolos.csv`), cada token de fechamento (`)`, `}`, `]`) indica explicitamente o **ID** do seu respectivo token de abertura na coluna chamada **`Ref`**.
   - Para os demais tokens e tokens de abertura, a coluna `Ref` permanece vazia.

3. **Verificação de Aninhamento (LIFO):**
   - Utilização de uma estrutura de pilha para validar que os blocos abertos mais recentemente são fechados primeiro, impedindo aninhamentos inválidos como `( [ ) ]` ou fechamentos órfãos.

---

## 2. Estrutura dos Arquivos

- **`analisador.py`**: Código-fonte do analisador léxico, sintático (com pilha) e gerador do relatório e CSV.
- **`input.c`**: Código-fonte de teste em C contendo estruturas de vetores, matrizes, expressões aninhadas e blocos.
- **`tabela_simbolos.csv`**: Tabela de símbolos no formato `ID;token;tipo;linha;coluna;Ref`.
- **`gramatica.txt`**: Fundamentação teórica do autômato com pilha e linguagem de delimitadores balanceados.

---

## 3. Como Executar

No terminal (PowerShell ou Prompt de Comando) na pasta `analiseSintaticaExercicio2Anthony`:

```powershell
py analisador.py
```

O programa exibirá:
1. **Varredura Léxica Linha a Linha:** exibindo tokens, tipos, posições e referências imediatas.
2. **Quadro Comparativo de Contagens:** tabela mostrando quantidades de abertura, fechamento, diferença e status de contagem idêntica.
3. **Mapeamento de Pares na Pilha:** lista com os pares associados `Fecha -> Abre (Ref)`.
4. **Veredito Sintático:** confirmação de aceitação ou lista detalhada de erros caso haja inconsistência.
5. **Geração do CSV:** gravação atualizada em `tabela_simbolos.csv`.
