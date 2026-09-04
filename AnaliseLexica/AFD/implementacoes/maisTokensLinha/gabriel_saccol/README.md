# Analisador Léxico - Atualização (Gabriel Saccol)

## O que foi modificado

1. **Múltiplos tokens por linha**: `processarArquivo` agora varre cada linha
   caractere a caractere, separando os tokens por espaços em branco (ao invés
   de tratar a linha inteira como um único termo). Cada token é reconhecido
   individualmente pelo AFD.

2. **Coluna do token**: cada entrada da tabela de símbolos agora registra
   também a coluna (posição, em caracteres, 1-based) em que o token começa
   na linha original.

3. **Correção de bug**: o método antigo usava uma variável `tipo` que nunca
   era declarada em `processarArquivo` (erro de compilação). Isso foi
   corrigido: `reconheceTermo` agora retorna diretamente o tipo do token
   (ou `null` se não reconhecido), e o tipo "ERRO" é usado na tabela para
   tokens inválidos, sem interromper o processamento das próximas linhas.

4. **Novos tipos de token no AFD** (arquivo `AFD_config.txt`):
   - `INTEIRO` (já existia)
   - `FRACIONARIO` (já existia)
   - `NOMEVARIAVEL` (já existia)
   - `ATRIBUICAO` → símbolo `=`
   - `SINAL_COMPARACAO` → símbolos `<`, `>`, `==`, `<=`, `>=`
   - `VIRGULA` → símbolo `,`
   - `PONTO_VIRGULA` → símbolo `;`

   Novos estados adicionados ao AFD: `Q7` (ATRIBUICAO), `Q8`
   (SINAL_COMPARACAO, para `==`, `<=`, `>=`), `Q9` e `Q10` (SINAL_COMPARACAO,
   para `<` e `>` isolados), `Q11` (VIRGULA) e `Q12` (PONTO_VIRGULA).

5. **Tabela de símbolos** agora possui as colunas: `ID`, `Token`, `Tipo`,
   `Linha` e `Coluna` (tanto no `System.out` quanto no HTML exportado).

## Como executar

Requer JDK instalado (o ambiente de teste local só tinha JRE, então o
código foi validado por simulação da lógica do AFD, mas segue os mesmos
padrões de compilação Java do projeto original).

```bash
javac ReconhecedorAFD.java
java ReconhecedorAFD
```

Isso lê `AFD_config.txt` (configuração do AFD) e `input.c` (arquivo de
entrada com múltiplos tokens por linha), e gera `tabelaSimbolos.html` com
a tabela de símbolos resultante.

## Arquivos

- `ReconhecedorAFD.java` — código-fonte atualizado
- `AFD_config.txt` — configuração do AFD com os novos tipos de token
- `input.c` — arquivo de teste com várias linhas e múltiplos tokens por linha
