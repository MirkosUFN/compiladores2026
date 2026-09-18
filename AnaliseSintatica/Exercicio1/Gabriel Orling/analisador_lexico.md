# Gramática de Declaração e Inicialização de Variáveis por Tipo

## 0. Terminais e Símbolos Léxicos Base

```text
[SATR]       -> =  (Sinal de Atribuição)
[PV]         -> ;  (Ponto e Vírgula)
[VG]         -> ,  (Vírgula)
[NOMEVAR]    -> Letra (Letra | Digito | _ )*
[NUM_INT]    -> Digito+
[NUM_FLOAT]  -> Digito+ . Digito+
[CARACTERE]  -> ' Letra | Digito | Símbolo '
[VAL_BOOL]   -> true | false
```

---

## 1. Tipo Inteiro (`int`)

**PALAVRA RESERVADA:** `[PR:INT] -> int`

### Regras de Formação
```text
ItemInt          -> [NOMEVAR] | [NOMEVAR] [SATR] [NUM_INT]
ListaItemInt     -> ItemInt | ItemInt [VG] ListaItemInt
```

### Formas de Declaração
```text
DecInt           -> [PR:INT] [NOMEVAR] [PV]
DecIniInt        -> [PR:INT] [NOMEVAR] [SATR] [NUM_INT] [PV]
DecMultiInt      -> [PR:INT] [NOMEVAR] [VG] ListaItemInt [PV] 
DecIniMultiInt   -> [PR:INT] ItemInt [VG] ListaItemInt [PV]
```

### Exemplos
```c
int x;                        // DecInt
int x = 10;                   // DecIniInt
int x, y, z;                  // DecMultiInt
int x = 10, y = 5, z;         // DecIniMultiInt
```

---

## 2. Tipo Fracionário (`float`)

**PALAVRA RESERVADA:** `[PR:FLOAT] -> float`

### Regras de Formação
```text
ItemFloat        -> [NOMEVAR] | [NOMEVAR] [SATR] [NUM_FLOAT]
ListaItemFloat   -> ItemFloat | ItemFloat [VG] ListaItemFloat
```

### Formas de Declaração
```text
DecFloat         -> [PR:FLOAT] [NOMEVAR] [PV]
DecIniFloat      -> [PR:FLOAT] [NOMEVAR] [SATR] [NUM_FLOAT] [PV]
DecMultiFloat    -> [PR:FLOAT] [NOMEVAR] [VG] ListaItemFloat [PV]
DecIniMultiFloat -> [PR:FLOAT] ItemFloat [VG] ListaItemFloat [PV]
```

### Exemplos
```c
float area;                               // DecFloat
float pi = 3.14;                          // DecIniFloat
float peso, altura;                       // DecMultiFloat
float a = 1.5, b, c = 2.0;                // DecIniMultiFloat
```

---

## 3. Tipo Fracionário Duplo (`double`)

**PALAVRA RESERVADA:** `[PR:DOUBLE] -> double`

### Regras de Formação
```text
ItemDouble       -> [NOMEVAR] | [NOMEVAR] [SATR] [NUM_FLOAT]
ListaItemDouble  -> ItemDouble | ItemDouble [VG] ListaItemDouble
```

### Formas de Declaração
```text
DecDouble         -> [PR:DOUBLE] [NOMEVAR] [PV]
DecIniDouble      -> [PR:DOUBLE] [NOMEVAR] [SATR] [NUM_FLOAT] [PV]
DecMultiDouble    -> [PR:DOUBLE] [NOMEVAR] [VG] ListaItemDouble [PV]
DecIniMultiDouble -> [PR:DOUBLE] ItemDouble [VG] ListaItemDouble [PV]
```

### Exemplos
```c
double saldo;                                   // DecDouble
double taxa = 0.0054;                           // DecIniDouble
double x, y, z;                                 // DecMultiDouble
double valor = 100.50, desconto, total = 90.45; // DecIniMultiDouble
```

---

## 4. Tipo Caractere (`char`)

**PALAVRA RESERVADA:** `[PR:CHAR] -> char`

### Regras de Formação
```text
ItemChar         -> [NOMEVAR] | [NOMEVAR] [SATR] [CARACTERE]
ListaItemChar    -> ItemChar | ItemChar [VG] ListaItemChar
```

### Formas de Declaração
```text
DecChar          -> [PR:CHAR] [NOMEVAR] [PV]
DecIniChar       -> [PR:CHAR] [NOMEVAR] [SATR] [CARACTERE] [PV]
DecMultiChar     -> [PR:CHAR] [NOMEVAR] [VG] ListaItemChar [PV]
DecIniMultiChar  -> [PR:CHAR] ItemChar [VG] ListaItemChar [PV]
```

### Exemplos
```c
char letra;                               // DecChar
char vogal = 'a';                         // DecIniChar
char op1, op2;                            // DecMultiChar
char sexo = 'M', status, tipo = 'X';      // DecIniMultiChar
```

---

## 5. Tipo Booleano (`boolean` / `bool`)

**PALAVRA RESERVADA:** `[PR:BOOLEAN] -> boolean | bool`

### Regras de Formação
```text
ItemBool         -> [NOMEVAR] | [NOMEVAR] [SATR] [VAL_BOOL]
ListaItemBool    -> ItemBool | ItemBool [VG] ListaItemBool
```

### Formas de Declaração
```text
DecBool          -> [PR:BOOLEAN] [NOMEVAR] [PV]
DecIniBool       -> [PR:BOOLEAN] [NOMEVAR] [SATR] [VAL_BOOL] [PV]
DecMultiBool     -> [PR:BOOLEAN] [NOMEVAR] [VG] ListaItemBool [PV]
DecIniMultiBool  -> [PR:BOOLEAN] ItemBool [VG] ListaItemBool [PV]
```

### Exemplos
```c
boolean ativo;                                     // DecBool
boolean logado = true;                             // DecIniBool
bool flag1, flag2;                                 // DecMultiBool
bool validado = false, testado, concluido = true;  // DecIniMultiBool
```
