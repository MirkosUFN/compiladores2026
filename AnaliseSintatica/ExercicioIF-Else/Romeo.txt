Árvore de Derivação:
  └── SIF
      ├── [PR:IF]: if
      ├── [AP]: (
      ├── [CONDICAO]
      │   ├── [NOMEVAR]: x
      │   ├── [COMPARACAO]: >
      │   └── [VALOR]
      │       └── INTEIRO: 0
      ├── [FP]: )
      ├── [ACH]: {
      ├── [BLOCO]
      │   └── SIF
      │       ├── [PR:IF]: if
      │       ├── [AP]: (
      │       ├── [CONDICAO]
      │       │   ├── [NOMEVAR]: y
      │       │   ├── [COMPARACAO]: >
      │       │   └── [VALOR]
      │       │       └── INTEIRO: 0
      │       ├── [FP]: )
      │       ├── [ACH]: {
      │       ├── [BLOCO]
      │       │   └── ATRIB
      │       │       ├── [NOMEVAR]: w
      │       │       ├── [ATRIBUICAO]: =
      │       │       ├── [VALOR]
      │       │       │   └── INTEIRO: 10
      │       │       └── [PONTOEVIRGULA]: ;
      │       └── [FCH]: }
      └── [FCH]: }
