# Análise de alocação de memória — código em C

## 1. Elementos alocados em memória

No trecho de código fornecido, temos:

| Elemento | Tipo |
|----------|------|
| `a` | `int` (variável local) |
| `b` | `int` (variável local) |
| `"%d + %d = %d"` | string literal (`char[]`) |

## 2. Tamanho dos tipos

- `int` = **4 bytes** (32 bits)
- `char` = **1 byte**

## 3. Cálculo da memória para DADOS

### Variáveis locais (stack)

```
a (int) = 4 bytes
b (int) = 4 bytes
----------------------
Subtotal variáveis = 8 bytes
```

### String literal (segmento de dados somente leitura)

A string `"%d + %d = %d"` contém:

| Caractere | Bytes |
|-----------|-------|
| `%` | 1 |
| `d` | 1 |
| ` ` (espaço) | 1 |
| `+` | 1 |
| ` ` (espaço) | 1 |
| `%` | 1 |
| `d` | 1 |
| ` ` (espaço) | 1 |
| `=` | 1 |
| ` ` (espaço) | 1 |
| `%` | 1 |
| `d` | 1 |
| `\0` (terminador nulo) | 1 |
| **Total** | **13 bytes** |

### Total de DADOS

```
Variáveis locais (a, b)  =  8 bytes
String literal           = 13 bytes
------------------------------------
Total                    = 21 bytes
```

## 5. Conclusão

| Item | Tipo | Memória |
|------|------|---------|
| `a` | `int` | 4 bytes |
| `b` | `int` | 4 bytes |
| `"%d + %d = %d"` | `char[13]` | 13 bytes |
| **Total de DADOS** | | **21 bytes** |