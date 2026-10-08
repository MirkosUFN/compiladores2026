# 📚 Compiladores - Análise Sintática

## 📝 Exercício 1: Sintaxe de Declaração e Inicialização de Variáveis

---

### 📌 Enunciado
> A partir da sintaxe original de declaração de variável abaixo, criar uma **NOVA SINTAXE** para declaração com inicialização de variável.

#### Sintaxe Original:
```bnf
[TIPO] -> PR:INT | PR:CHAR | PR:FLOAT | PR:DOUBLE | PR:VOID | PR:BOOLEAN
Declara -> [TIPO][NOMEVARIAVEL][PV] | [TIPO][NOMEVARIAVEL] DeclaraMultiplo [PV]
DeclaraMultiplo -> [VG][NOMEVARIAVEL] | [VG][NOMEVARIAVEL] DeclaraMultiplo

DeclaraIni -> DecIniInt | DecIniFrac | DecIniChar | DecIniBool
DecIniInt -> PR:INT [NOMEVARIAVEL][SATR][INTEIRO][PV] | PR:INT [NOMEVARIAVEL][SATR][INTEIRO][REPINIINT][PV]
REPINIINT -> [VG][NOMEVARIAVEL][SATR][INTEIRO] | [VG][NOMEVARIAVEL][SATR][INTEIRO][REPINIINT]
DecIniFrac -> PR:FLOAT [NOMEVARIAVEL][SATR][FRACIONARIO][PV] | PR:FLOAT [NOMEVARIAVEL][SATR][FRACIONARIO][REPINIFRAC][PV]|
              PR:DOUBLE [NOMEVARIAVEL][SATR][FRACIONARIO][PV] | PR:DOUBLE [NOMEVARIAVEL][SATR][FRACIONARIO][REPINIFRAC][PV]
REPINIFRAC -> [VG][NOMEVARIAVEL][SATR][FRACIONARIO] | [VG][NOMEVARIAVEL][SATR][FRACIONARIO][REPINIFRAC]
DecIniChar -> PR:Char [NOMEVARIAVEL][SATR][ASPAS][CARACTER][ASPAS][PV] | PR:Char [NOMEVARIAVEL][SATR][ASPAS][CARACTER][ASPAS][REPINICHAR][PV]
REPINICHAR -> [VG][NOMEVARIAVEL][SATR][ASPAS][CARACTER][ASPAS] | [VG][NOMEVARIAVEL][SATR][ASPAS][CARACTER][ASPAS] [REPINICHAR]
DecIniBool -> PR:Boolean [NOMEVARIAVEL][SATR] PR:TRUE | PR:Boolean [NOMEVARIAVEL][SATR] PR:FALSE |
              PR:Boolean [NOMEVARIAVEL][SATR] PR:TRUE [REPINIBOOL]| PR:Boolean [NOMEVARIAVEL][SATR] PR:FALSE [REPINIBOOL]
REPINIBOOL -> [VG][NOMEVARIAVEL][SATR] PR:TRUE | [VG][NOMEVARIAVEL][SATR] PR:FALSE | [VG][NOMEVARIAVEL][SATR] PR:TRUE [REPINIBOOL] |
              [VG][NOMEVARIAVEL][SATR] PR:FALSE [REPINIBOOL]
```

---

### 🔍 1. Análise Crítica da Sintaxe Original

A sintaxe original possui limitações conceituais e estruturais que tornam a gramática inchada e inflexível:

1. **Acoplamento entre Sintaxe e Semântica (Explosão de Regras)**:
   - Em teoria de compiladores, a verificação de compatibilidade de tipos (ex: atribuir um inteiro a uma variável inteira) é responsabilidade da **Análise Semântica**, e não da **Análise Sintática**.
   - Ao tentar amarrar cada tipo ao seu respectivo valor literal na gramática, surgiram 14 produções redundantes (`DecIniInt`, `DecIniFrac`, `DecIniChar`, `DecIniBool`, etc.).
2. **Inflexibilidade (Sem suporte à declaração mista)**:
   - A sintaxe original força que ou **todas** as variáveis sejam não-inicializadas (`Declara`) ou **todas** sejam inicializadas (`DeclaraIni`).
   - Não permite construções comuns em linguagens de programação, tais como: `int a, b = 10, c;`.
3. **Inconsistências Sintáticas**:
   - As produções de `DecIniBool` não finalizam com `[PV]` (ponto e vírgula).
   - Inconsistência nos identificadores de tokens: `PR:Char` e `PR:Boolean` com letras minúsculas vs `PR:INT`, `PR:FLOAT`, `PR:DOUBLE`, etc.
   - O tipo `PR:VOID` está presente em `[TIPO]`, porém variáveis do tipo `void` não devem aceitar inicialização de valores diretos.

---

### 💡 2. Nova Sintaxe Proposta (Solução Ideal: Modular e Unificada)

A abordagem ideal unifica a declaração e a inicialização através da abstração do conceito de **`[VALOR]`** e de uma regra que permite que a atribuição seja **opcional** para cada variável.

#### 🏷️ Tabela de Tokens e Símbolos
| Token / Símbolo | Significado | Exemplo |
| :--- | :--- | :--- |
| `[TIPO]` | Tipo de dado primitivo | `int`, `float`, `double`, `char`, `boolean` |
| `[NOMEVARIAVEL]` | Identificador da variável | `x`, `total`, `media` |
| `[SATR]` | Símbolo de atribuição | `=` |
| `[VG]` | Vírgula (separador) | `,` |
| `[PV]` | Ponto e vírgula (terminador) | `;` |
| `[VALOR]` | Literal ou constante | `10`, `3.14`, `'A'`, `true`, `false` |

---

#### 🌟 2.1. Gramática em BNF (Forma de Backus-Naur)

```bnf
# 1. Definição de Tipos Válidos para Variáveis
[TIPO] -> PR:INT | PR:CHAR | PR:FLOAT | PR:DOUBLE | PR:BOOLEAN

# 2. Definição Genérica de Valores / Literais
[VALOR] -> [INTEIRO] | [FRACIONARIO] | [ASPAS][CARACTER][ASPAS] | PR:TRUE | PR:FALSE

# 3. Declaração Geral (com ou sem inicialização)
Declara -> [TIPO] ItemVar [PV] | [TIPO] ItemVar RepeticaoVar [PV]

# 4. Item de Variável: Pode ser apenas o nome OU acompanhado de atribuição
ItemVar -> [NOMEVARIAVEL] | [NOMEVARIAVEL] [SATR] [VALOR]

# 5. Recursão para Múltiplas Variáveis
RepeticaoVar -> [VG] ItemVar | [VG] ItemVar RepeticaoVar
```

> **Por que esta solução é superior?**
> - **Redução de 14 para 5 produções**, garantindo facilidade de manutenção.
> - **Suporte a declaração mista**: aceita `int a;`, `int a = 5;` e `int a, b = 2, c;`.
> - **Separação correta de fases do compilador**: a sintaxe cuida da estrutura do código e a semântica cuida da compatibilidade de tipos.

---

#### 📐 2.2. Equivalente em EBNF (Forma Estendida de Backus-Naur)
Utilizando os operadores `?` (opcional: zero ou uma vez) e `*` (repetição: zero ou mais vezes):

```ebnf
Declara -> [TIPO] [NOMEVARIAVEL] ([SATR] [VALOR])? ([VG] [NOMEVARIAVEL] ([SATR] [VALOR])?)* [PV]
```

---

### 🎯 3. Variação: Sintaxe Exclusiva para Declaração COM Inicialização

Caso o objetivo específico seja substituir apenas o bloco `DeclaraIni` (onde **toda** variável declarada deve obrigatoriamente ser inicializada):

```bnf
# Tipos e Valores
[TIPO] -> PR:INT | PR:CHAR | PR:FLOAT | PR:DOUBLE | PR:BOOLEAN
[VALOR] -> [INTEIRO] | [FRACIONARIO] | [ASPAS][CARACTER][ASPAS] | PR:TRUE | PR:FALSE

# Declaração Inicializada Genérica
DeclaraIni -> [TIPO] ItemIni [PV] | [TIPO] ItemIni RepeticaoIni [PV]
ItemIni -> [NOMEVARIAVEL] [SATR] [VALOR]
RepeticaoIni -> [VG] ItemIni | [VG] ItemIni RepeticaoIni
```

---

### 🔬 4. Variação: Mantendo a Checagem de Tipos no Nível Sintático

Se a intenção pedagógica da disciplina for manter a restrição de tipos expressa diretamente na sintaxe livre de contexto, podemos corrigir os erros da sintaxe original (como a ausência de `[PV]` no booleano) e permitir declarações com ou sem inicialização de forma estruturada:

```bnf
Declara -> DecInt | DecFrac | DecChar | DecBool

# --- Inteiros ---
DecInt  -> PR:INT ItemInt [PV] | PR:INT ItemInt RepInt [PV]
ItemInt -> [NOMEVARIAVEL] | [NOMEVARIAVEL] [SATR] [INTEIRO]
RepInt  -> [VG] ItemInt | [VG] ItemInt RepInt

# --- Fracionários (float e double) ---
TipoFrac -> PR:FLOAT | PR:DOUBLE
DecFrac  -> TipoFrac ItemFrac [PV] | TipoFrac ItemFrac RepFrac [PV]
ItemFrac -> [NOMEVARIAVEL] | [NOMEVARIAVEL] [SATR] [FRACIONARIO]
RepFrac  -> [VG] ItemFrac | [VG] ItemFrac RepFrac

# --- Caracteres ---
DecChar  -> PR:CHAR ItemChar [PV] | PR:CHAR ItemChar RepChar [PV]
ItemChar -> [NOMEVARIAVEL] | [NOMEVARIAVEL] [SATR] [ASPAS][CARACTER][ASPAS]
RepChar  -> [VG] ItemChar | [VG] ItemChar RepChar

# --- Booleanos ---
DecBool   -> PR:BOOLEAN ItemBool [PV] | PR:BOOLEAN ItemBool RepBool [PV]
ItemBool  -> [NOMEVARIAVEL] | [NOMEVARIAVEL] [SATR] ValorBool
ValorBool -> PR:TRUE | PR:FALSE
RepBool   -> [VG] ItemBool | [VG] ItemBool RepBool
```

---

### 🧪 5. Exemplos de Derivação (Validação da Nova Sintaxe)

Demonstração de derivações utilizando a **Sintaxe Unificada (Seção 2.1)**:

#### Exemplo 1: `int x = 10;`
1. `Declara`
2. `=> [TIPO] ItemVar [PV]`
3. `=> PR:INT ItemVar [PV]`
4. `=> PR:INT [NOMEVARIAVEL] [SATR] [VALOR] [PV]`
5. `=> PR:INT [NOMEVARIAVEL] [SATR] [INTEIRO] [PV]`

---

#### Exemplo 2: `float a, b = 3.14, c;` *(Declaração Mista)*
1. `Declara`
2. `=> [TIPO] ItemVar RepeticaoVar [PV]`
3. `=> PR:FLOAT [NOMEVARIAVEL] RepeticaoVar [PV]` *(Variável 'a')*
4. `=> PR:FLOAT [NOMEVARIAVEL] [VG] ItemVar RepeticaoVar [PV]`
5. `=> PR:FLOAT [NOMEVARIAVEL] [VG] [NOMEVARIAVEL] [SATR] [VALOR] RepeticaoVar [PV]`
6. `=> PR:FLOAT [NOMEVARIAVEL] [VG] [NOMEVARIAVEL] [SATR] [FRACIONARIO] RepeticaoVar [PV]` *(Variável 'b = 3.14')*
7. `=> PR:FLOAT [NOMEVARIAVEL] [VG] [NOMEVARIAVEL] [SATR] [FRACIONARIO] [VG] ItemVar [PV]`
8. `=> PR:FLOAT [NOMEVARIAVEL] [VG] [NOMEVARIAVEL] [SATR] [FRACIONARIO] [VG] [NOMEVARIAVEL] [PV]` *(Variável 'c')*

---

#### Exemplo 3: `boolean ativo = true, flag = false;`
1. `Declara`
2. `=> [TIPO] ItemVar RepeticaoVar [PV]`
3. `=> PR:BOOLEAN [NOMEVARIAVEL] [SATR] [VALOR] RepeticaoVar [PV]`
4. `=> PR:BOOLEAN [NOMEVARIAVEL] [SATR] PR:TRUE [VG] ItemVar [PV]`
5. `=> PR:BOOLEAN [NOMEVARIAVEL] [SATR] PR:TRUE [VG] [NOMEVARIAVEL] [SATR] [VALOR] [PV]`
6. `=> PR:BOOLEAN [NOMEVARIAVEL] [SATR] PR:TRUE [VG] [NOMEVARIAVEL] [SATR] PR:FALSE [PV]`

---

### 📊 6. Tabela Comparativa

| Critério | Sintaxe Original | Nova Sintaxe (Proposta) |
| :--- | :--- | :--- |
| **Quantidade de regras** | 14 regras | **5 regras** |
| **Declaração mista** (`int a, b = 1;`) | ❌ Não suporta | ✅ Totalmente suportada |
| **Separação de responsabilidades** | ❌ Mistura sintaxe e semântica | ✅ Foco puramente sintático |
| **Extensibilidade para novos tipos** | ❌ Exige criar novas produções duplicadas | ✅ Basta adicionar o novo tipo em `[TIPO]` |
| **Erros sintáticos corrigidos** | ❌ Falta `[PV]` no booleano | ✅ Consistente e corrigido |
