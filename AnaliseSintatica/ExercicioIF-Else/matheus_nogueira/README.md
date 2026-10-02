# Árvore de derivação — IF aninhado

Esta pasta contém a árvore de derivação da sentença definida em:

```c
if(x>0){
  if(y>0){
    w=10;
  }
}
```

A gramática utilizada está no arquivo `readme.txt` da pasta pai. O símbolo
`SIF` representa uma sentença `if`, e `PR:IF` representa a palavra reservada
`if`.

## Arquivos

### `arvore_derivacao.py`

Código Python que constrói a árvore de derivação usando a gramática do
exercício. Ao ser executado, ele:

- imprime a árvore no terminal;
- gera `arvore_derivacao.txt` em formato de texto;
- gera `arvore_derivacao.dot` em formato Graphviz.

O código utiliza apenas bibliotecas padrão do Python.

### `arvore_derivacao.txt`

Versão textual da árvore, que pode ser lida diretamente no editor ou no
terminal.

### `arvore_derivacao.dot`

Descrição da árvore no formato DOT, utilizado pelo Graphviz para criar uma
imagem ou um PDF.

### `arvore_derivacao.png` ou `arvore_derivacao.svg`

Esses arquivos não são obrigatórios e são gerados a partir do `.dot` usando o
Graphviz.

## Executar o código Python

A partir desta pasta:

```bash
python3 arvore_derivacao.py
```

Ou, a partir da raiz do repositório:

```bash
python3 AnaliseSintatica/ExercicioIF-Else/matheus_nogueira/arvore_derivacao.py
```

## Instalar o Graphviz

O Graphviz é o programa que interpreta o arquivo `.dot`. O Python não precisa
de uma biblioteca adicional para gerar o arquivo DOT.

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install graphviz
```

### Fedora

```bash
sudo dnf install graphviz
```

### Windows

Com `winget`:

```powershell
winget install Graphviz.Graphviz
```

Depois da instalação, feche e abra o terminal novamente e verifique:

```bash
dot -V
```

## Gerar a imagem

Entre na pasta da implementação:

```bash
cd AnaliseSintatica/ExercicioIF-Else/matheus_nogueira
```

Gere uma imagem PNG:

```bash
dot -Tpng arvore_derivacao.dot -o arvore_derivacao.png
```

Gere uma imagem SVG, que pode ser ampliada sem perder qualidade:

```bash
dot -Tsvg arvore_derivacao.dot -o arvore_derivacao.svg
```

Gere um PDF:

```bash
dot -Tpdf arvore_derivacao.dot -o arvore_derivacao.pdf
```

Para abrir o PNG no Linux:

```bash
xdg-open arvore_derivacao.png
```

No VS Code, basta abrir o arquivo gerado `arvore_derivacao.png` ou
`arvore_derivacao.svg` no explorador de arquivos.
