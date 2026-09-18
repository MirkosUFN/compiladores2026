# Como Utilizar o Analizador de Linguagens Para Qualquer Linguagem

## Arquivos de Configuração

o automato precisa dos seguintes arquivos de configuração para cada linguagem já pré criados
* arquivo de configurações do AFD (Automato Finito Deterministico)
* arquivo de listagem de palavras reservadas
* arquivo com regras de sintaxe

### arquivo de configurações do AFD (Automato Finito Deterministico)

Nesse arquivo é estipulado as configurações basicas do automato, ou seja, caracteres, nós (inicial, finais e auxiliares) e regras de transição

estrutura:
* linha 1: todos os estados separados por espaço, sendo o primeiro estado o estado inicial
* linha 2: todos os estados finais e o tipo de valor (do seguinte modelo `[estado]:[tipo de valor]`) separados por espaço
* linha 3: todos caracteres aceitos pelo automato separados por espaço
* linha 4+: todas as regras de transição (uma abaixo da outra) no seguinte modelo `[estado de partida]:[caractere]:[estado destino]`

### arquivo de listagem de palavras reservadas

Nesse arquivo é escolhido quais são as palavras reservadas do programa, a listagem deve ser feita uma a baixo da outra

### arquivo com regras de sintaxe

Nesse arquivo é estipulado todas as regras de sintaxe da linguagem, a listagem deve ser feita uma a baixo da outra

Regras para escrever sintaxe
* Se referir a algum tipo estipulado no arquivo de configuração: `[[[nome do tipo]]]`
* se referir a alguma palavra reservada estipulada no arquivo de seleção dele palavras reservadas: `[[PR:[a palavra reservada]]]`
* se referir a alguma regra de sintaxe: `[regra de sintaxe]`
* como criar uma regra: `[nome da regra] -> [regra]`
* como criar mais de uma possibilidade para a mesma regra: `[nome da regra] -> [padrão 1] | [padrão 2]`
  * o pipe serve para dizer ou, nesse caso, ele diz que o programa vai seguir o padrão 1, se não bater, ele vai tentar com a padrão 2
  * uma mesma regra pode ter inumeros padrões, separado por um pipe
* como fazer recursão: `[nome da regra] -> ...[nome de alguma regra]...`



