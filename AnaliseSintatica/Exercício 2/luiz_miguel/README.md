# Analisador Sintático, Léxico e Balanceador de Delimitadores

Esta implementação atende às especificações da análise sintática, léxica e validação de delimitadores aninhados `( )`, `{ }` e `[ ]`. 

O sistema conta com **suporte a pilhas para validação de delimitadores**, preenchimento da coluna **`Ref`** na Tabela de Símbolos, exibição da **Árvore de Derivação Sintática** e geração do relatório em formato CSV e tabelas ASCII no terminal.

---

## 1. Regras de Delimitadores e Sintaxe

### Balanceamento de Delimitadores
- Os tokens de abertura `(`, `{` e `[` devem ter uma contagem e aninhamento exatamente correspondente aos tokens de fechamento `)`, `}` e `]`.
- Na **Tabela de Símbolos**, para cada token de **fechamento**, a coluna `Ref` indica o **ID** do token de **abertura** correspondente.

### Gramática Registrada (`sintaxe.txt`)

O arquivo [`sintaxe.txt`](sintaxe.txt) define a gramática reconhecida pelo analisador:

```text
# Tipos definidos no enunciado
[TIPO] -> PR:INT | PR:CHAR | PR:FLOAT | PR:DOUBLE | PR:VOID | PR:BOOLEAN

# Valores e Identificadores
[VALOR] -> INTEIRO | FRACIONARIO | NOMEVARIAVEL | PR:TRUE | PR:FALSE | LITERAL_CARACTERE | LITERAL_TEXTO

# Operadores e Delimitadores
[ATRIBUICAO] -> '='
[SINAL_COMPARACAO] -> '>' | '<' | '>=' | '<=' | '==' | '!='
[DELIMITADORES] -> ABRE_PARENTESE | FECHA_PARENTESE | ABRE_CHAVE | FECHA_CHAVE | ABRE_COLCHETE | FECHA_COLCHETE | PONTO_VIRGULA | VIRGULA

# Estrutura do Programa e Comandos
Programa -> ListaComandos
ListaComandos -> Comando | Comando ListaComandos
Comando -> Condicional | Atribuicao | Declara | Bloco

# Regras de Estrutura Condicional (IF / Blocos aninhados)
Condicional -> PR:IF ABRE_PARENTESE ExpressaoRelacional FECHA_PARENTESE Bloco | PR:IF ABRE_PARENTESE ExpressaoRelacional FECHA_PARENTESE Bloco PR:ELSE Bloco | PR:IF ABRE_PARENTESE ExpressaoRelacional FECHA_PARENTESE Comando

# Regras de Delimitadores de Bloco e Aninhamento
Bloco -> ABRE_CHAVE ListaComandos FECHA_CHAVE | ABRE_CHAVE FECHA_CHAVE
Delimitador -> Parenteses | Chaves | Colchetes
Parenteses -> ABRE_PARENTESE Conteudo FECHA_PARENTESE
Chaves -> ABRE_CHAVE Conteudo FECHA_CHAVE
Colchetes -> ABRE_COLCHETE Conteudo FECHA_COLCHETE

# Regras de Expressão e Comparação
ExpressaoRelacional -> VALOR SINAL_COMPARACAO VALOR

# Regra de Comando de Atribuição Simples
Atribuicao -> NOMEVARIAVEL ATRIBUICAO VALOR PONTO_VIRGULA

# Regras de Declaração de Variáveis (com ou sem inicialização)
[INICIALIZACAO] -> ATRIBUICAO VALOR
[DECLARADOR] -> NOMEVARIAVEL | NOMEVARIAVEL INICIALIZACAO
Declara -> TIPO DECLARADOR PONTO_VIRGULA | TIPO DECLARADOR DeclaraMultiplo PONTO_VIRGULA
DeclaraMultiplo -> VIRGULA DECLARADOR | VIRGULA DECLARADOR DeclaraMultiplo