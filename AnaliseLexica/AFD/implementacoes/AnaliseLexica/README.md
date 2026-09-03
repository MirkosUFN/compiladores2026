# Analisador Léxico com AFD

Analisador léxico simples, onde o autômato (AFD) é totalmente definido pelo
arquivo `configAfd.md`, sem regras fixas no código.

## Arquivos

- `configAfd.md` — configuração do AFD (estados, alfabeto, estados finais/tokens e regras de transição). Reconhece:
  - `INTEIRO` (ex: `30`, `-8`)
  - `FRACIONARIO` (ex: `3.5`, `-0.1`)
  - `NOMEVARIAVEL` (ex: `abc`, `_oi`, `nome123`)
- `analisador_lexico.py` — lê `configAfd.md`, monta o AFD e simula-o sobre um arquivo de entrada, gerando a tabela de símbolos.
- `entrada.txt` — arquivo de exemplo com vários termos, incluindo casos com espaços múltiplos, tabs, linhas em branco e termos inválidos (para testar a rejeição).
- `tabela_simbolos.csv` — gerado automaticamente ao rodar o script.

## Como rodar

```bash
python analisador_lexico.py
```

Ou apontando arquivos específicos:

```bash
python analisador_lexico.py configAfd.md entrada.txt
```
