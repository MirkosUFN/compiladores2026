### Estrutura Condicional Aninhada (IF Aninhado com Bloco)
Para:
```c
if(x>0){
  if(y>0){
    w=10;
    }
}
```

```text
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
      │       │   └── ...: w=10;
      │       └── [FCH]: }
      └── [FCH]: }
```

---
