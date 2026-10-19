# Exercício 2 — Balanceamento de delimitadores

Esta implementação valida os tokens `()`, `{}` e `[]` conforme o enunciado do Exercício 2:

- o número de **abre** de cada delimitador deve ser igual ao número de **fecha**;
- além da contagem, o analisador verifica com uma **pilha** se os delimitadores estão aninhados na ordem correta (`( [ ) ]` tem a mesma contagem, mas é inválido);
- na tabela de símbolos, cada fechamento indica na coluna `Ref` o token de abertura ao qual se refere.

## Tabela de símbolos

A tabela é gravada em `tabela_simbolos.csv` (separador `;`) com as colunas:

```
ID;token;tipo;linha;coluna;Ref
```

Para um token de fechamento, `Ref` recebe o `ID` do token de abertura correspondente. Os tokens de abertura e os demais tokens deixam essa coluna vazia.

Exemplo (trecho de `input.c`, linha 9 — `if ((v[i] % 2) == 0) {`):

| ID | token | tipo             | linha | coluna | Ref |
|----|-------|------------------|-------|--------|-----|
| 48 | (     | ABRE_PARENTESES  | 9     | 12     |     |
| 49 | (     | ABRE_PARENTESES  | 9     | 13     |     |
| 51 | [     | ABRE_COLCHETES   | 9     | 15     |     |
| 53 | ]     | FECHA_COLCHETES  | 9     | 17     | 51  |
| 56 | )     | FECHA_PARENTESES | 9     | 22     | 49  |
| 59 | )     | FECHA_PARENTESES | 9     | 28     | 48  |

> O token `;` aparece entre aspas (`";"`) no CSV porque ele é o próprio separador de colunas — o Excel e o LibreOffice leem normalmente.

## Execução

Na pasta desta implementação, execute:

```
python analisador_sintatico.py
```

O programa lê `input.c`, mostra os tokens no terminal, mostra a contagem de cada delimitador, valida o aninhamento e gera `tabela_simbolos.csv` na mesma pasta.

Também é possível passar outro arquivo de entrada:

```
python analisador_sintatico.py outro_arquivo.c
```

Se houver erro, o programa informa a linha e a coluna do problema, por exemplo:

```
Linha 1, coluna 10: ')' (ID 5) não corresponde a '[' (ID 4, linha 1, coluna 8).
Contagem de parênteses diferente: 2 abertura(s) e 1 fechamento(s).
```

## Arquivos

- `analisador_sintatico.py`: tokenização, validação com pilha e geração da tabela;
- `input.c`: entrada usada no exemplo;
- `sintaxe.txt`: representação das regras do exercício (contagem, gramática e algoritmo);
- `tabela_simbolos.csv`: tabela de símbolos gerada a partir de `input.c`.
