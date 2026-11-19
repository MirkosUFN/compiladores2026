# Análise Sintática — Exercício 2 — Bruno Difante

Execute python3 analisador_sintatico.py para analisar input.c e gerar
tabela_simbolos.csv. Para analisar outro arquivo, passe seu caminho na
linha de comando. Use --saida para indicar outro CSV.

A coluna Ref de cada fechamento válido contém o ID do token de
abertura correspondente. Uma pilha garante que os pares sejam fechados
na ordem correta. Por exemplo, ([)] tem as mesmas quantidades de
aberturas e fechamentos de cada tipo, mas é rejeitado. Delimitadores
dentro de comentários e literais não entram na pilha. Quando há erro,
o programa ainda grava o CSV e termina com código de saída 1.
