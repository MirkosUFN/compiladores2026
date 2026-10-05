# Exercício 2 — Balanceamento de ( ), { } e [ ] — Romeo Noro Guterres

O analisador verifica se os delimitadores `( )`, `{ }` e `[ ]` têm a mesma
quantidade de aberturas e fechamentos e se estão aninhados corretamente.
Na tabela de símbolos, cada fechamento indica na coluna **Ref** o `ID` do
token de abertura correspondente.

## Como funciona

1. **Léxico**: o arquivo `.c` vira uma lista de tokens (`ID`, lexema, tipo,
   linha, coluna). Delimitadores: `AP`/`FP` para parênteses, `ACH`/`FCH` para
   chaves e `ACO`/`FCO` para colchetes.
2. **Sintático (pilha)**: cada abertura é empilhada. Em cada fechamento, o
   topo da pilha é desempilhado; se for do mesmo tipo, o `ID` dele vai para a
   coluna `Ref` do fechamento. Se não for, o erro é reportado e o fechamento
   fica sem `Ref`. Aberturas que sobram na pilha no fim são erros.
3. A contagem de aberturas/fechamentos de cada par é exibida no terminal.

## Execução

```bash
python analisador_sintatico.py              # usa input.c -> tabela_simbolos.csv
python analisador_sintatico.py input_erros.c # -> tabela_simbolos_input_erros.csv
```

## Arquivos

- `analisador_sintatico.py`: léxico, verificação com pilha e geração da tabela;
- `sintaxe.txt`: gramática dos grupos delimitados;
- `input.c`: código correto (vetores, matriz, `if/else` e parênteses aninhados);
- `input_erros.c`: código com delimitadores trocados, sobrando e faltando;
- `tabela_simbolos.csv` / `tabela_simbolos_input_erros.csv`: tabelas geradas,
  com a coluna `Ref`.

## Exemplo (trecho de `tabela_simbolos.csv`)

```text
ID;token;tipo;linha;coluna;Ref
3;[;ACO;1;10;
5;];FCO;1;12;3
7;{;ACH;1;16;
13;};FCH;1;25;7
```
