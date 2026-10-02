# Analisador Léxico com AFD — Romeo Noro Guterres

O AFD é totalmente definido pelo arquivo `configAfd.md` (formato do enunciado),
então o programa não tem nenhuma regra de reconhecimento "fixa" no código.

## Tokens reconhecidos

| Estado final | Token        | Exemplos              |
|--------------|--------------|-----------------------|
| Q1           | INTEIRO      | `42`, `-17`, `+8`     |
| Q3           | FRACIONARIO  | `3.1415`, `-0.5`      |
| Q5           | NOMEVARIAVEL | `contador`, `_temp2`  |

Estados: `Q0` inicial, `Q4` após sinal `+`/`-`, `Q2` após o ponto decimal
(não final: `12.` é rejeitado).

## Execução

```bash
python analisador.py                         # usa configAfd.md e numeros.txt
python analisador.py outroAfd.md termos.txt  # arquivos alternativos
```

Cada termo é impresso com o tipo reconhecido ou o motivo do erro (símbolo fora
do alfabeto, transição inexistente ou parada em estado não final). Os termos
aceitos vão para `tabela_simbolos.csv` (`ID;token;tipo;linha;coluna`).
