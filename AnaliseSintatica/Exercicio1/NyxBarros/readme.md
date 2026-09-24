# AUTOMATO FINITO DETERMINISCITO PARA REALIZAR ANÁLISE LÉXICA

programa que faz de linguagems e que tem por foco ser de uso versátil para qualquer linguagem (podendo ser usado até para criar uma do zero)

## Executar o programa

* rodar o teste do compilador:

    ``` shell
    python3 -m teste.codigo
    ```

## Planejamento

Informações remetentes aos diagramas e funcionamentos podem ser visualizados em [planejamento](doc/planejamento.md)

## Usar com outras linguagens

O manual completo de como adaptar e utilizar o projeto para outras linguagens (ou até para uma linguagem que não existe oficialmente ainda) ser acessado pelo arquivo [como usar para outras linguagens.md](doc/como usar para outras linguagens.md)

## Arvore exemplo da analise sintatica:

Arvore: int nome, idade = 23, filhos = 3;

* DeclaraAtribuirInt:
  * int
  * AtribuirInt
    * nome
    * ,
    * AtribuirInt
      * idade
      * =
      * 23
      * ,
      * AtribuirInt
        * filhos
        * =
        * 3
        * ;