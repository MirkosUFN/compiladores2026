# Exercício — Análise Sintática: declaração de variável com inicialização

Analisador léxico/sintático em Python que reconhece declarações de variáveis
em um subconjunto de linguagem C-like, com duas gramáticas:

- **`Declara` / `DeclaraMultiplo`** (original, sem inicialização): `int a, b, c;`
- **`DeclaraIni`** (nova sintaxe, com inicialização): uma regra por tipo —
  `DecIniInt`, `DecIniFrac` (`float`/`double`), `DecIniChar`, `DecIniBool` —
  cada uma com seu `REPINI*` para múltiplas variáveis inicializadas na mesma
  linha (`int a = 1, b = 2;`). A gramática completa está em [`sintaxe.txt`](sintaxe.txt).

Diferente de uma regra genérica de "valor", cada `DecIni*` exige que o valor
atribuído seja do literal correspondente ao tipo declarado: `INTEIRO` só é
aceito para `int`, `FRACIONARIO` para `float`/`double`, `ASPAS CARACTER ASPAS`
(ex: `'a'`) para `char`, e `PR:TRUE`/`PR:FALSE` para `boolean`. `void` não
possui forma de inicialização. Declarações que misturam variáveis com e sem
`=` na mesma linha, ou com o literal errado para o tipo, são rejeitadas.

## Tipos suportados

`int`, `char`, `float`, `double`, `void`, `boolean`.

## Como rodar

```bash
python3 analisador_sintatico.py
```

O script lê `input.c`, imprime no terminal os tokens e o resultado
(ACEITA/REJEITADA) de cada linha, e grava a tabela de símbolos em
`tabela_simbolos.csv` (colunas `ID;token;tipo;linha;coluna`).

## Arquivos

- `analisador_sintatico.py` — tokenizador + parser.
- `sintaxe.txt` — gramática completa (original + nova sintaxe com inicialização).
- `input.c` — exemplos de entrada, incluindo casos válidos e inválidos de cada regra.
- `tabela_simbolos.csv` — gerado a cada execução.
