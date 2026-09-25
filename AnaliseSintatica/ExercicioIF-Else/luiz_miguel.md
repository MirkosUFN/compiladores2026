### Estrutura Condicional Aninhada (IF Aninhado com Bloco)
Para:
```c
if (x > 0) {
 if (y > 0) { z = 0 ; }
}
```

```text
Árvore de Derivação:
  └── Programa
      └── ListaComandos
          └── Comando
              └── Condicional
                  ├── [PR:IF]: if
                  ├── [AP]: (
                  ├── ExpressaoRelacional
                  │   ├── [VALOR]: x
                  │   ├── [SINAL_COMPARACAO]: >
                  │   └── [VALOR]: 0
                  ├── [FP]: )
                  └── Bloco
                      ├── [AC]: {
                      ├── ListaComandos
                      │   └── Comando
                      │       └── Condicional
                      │           ├── [PR:IF]: if
                      │           ├── [AP]: (
                      │           ├── ExpressaoRelacional
                      │           │   ├── [VALOR]: y
                      │           │   ├── [SINAL_COMPARACAO]: >
                      │           │   └── [VALOR]: 0
                      │           ├── [FP]: )
                      │           └── Bloco
                      │               ├── [AC]: {
                      │               ├── ListaComandos
                      │               │   └── Comando
                      │               │       └── Atribuicao
                      │               │           ├── [NOMEVARIAVEL]: z
                      │               │           ├── [ATRIBUICAO]: =
                      │               │           ├── [VALOR]: 0
                      │               │           └── [PV]: ;
                      │               └── [FC]: }
                      └── [FC]: }
```

---
