# Analisador Léxico com AFD

Implementação do exercício de [AnaliseLexica/AFD](https://github.com/MirkosUFN/compiladores2026/tree/main/AnaliseLexica/AFD).

## Arquivos

- `configAfd.md` — configuração do AFD (estados, alfabeto, estados finais/tokens e regras de transição), no formato definido pelo enunciado. Reconhece:
  - `INTEIRO` (ex: `30`, `-8`)
  - `FRACIONARIO` (ex: `3.5`, `-0.1`)
  - `NOMEVARIAVEL` (ex: `abc`, `_oi`, `nome123`)
- `analisador_lexico.py` — lê `configAfd.md`, monta o AFD e simula-o sobre um arquivo de entrada, gerando a tabela de símbolos.
- `entrada.txt` — arquivo de exemplo com vários termos (inclusive alguns inválidos, para testar a rejeição).
- `tabela_simbolos.csv` — gerado automaticamente ao rodar o script.

## Como rodar

```bash
python analisador_lexico.py
```

Ou apontando arquivos específicos:

```bash
python analisador_lexico.py configAfd.md entrada.txt
```

## O que foi completado em relação ao `configAfd.md` original do repositório

O arquivo de configuração fornecido no repositório só tinha regras de transição
completas para `INTEIRO` e `FRACIONARIO`; os estados `Q4` e `Q5` (sinal `+`/`-`
e nome de variável) apareciam listados mas sem transições. Neste
`configAfd.md` foram adicionadas as transições que faltavam:

- `Q0 --+/--> Q4 --dígito--> Q1` (número com sinal)
- `Q0 --letra/_--> Q5 --letra/dígito/_--> Q5` (nome de variável, podendo
  conter dígitos após o primeiro caractere)
