# notas auxiliares

'''c
    if(){
        if(){

        }else{
            if(){

            }
        }
    }else{if(){}
        else{ }
    }
'''

    Programa
    └── IfElse
            ├── "if"
            ├── "("
            ├── Condicao
            ├── ")"
            ├── "{"
            ├── Bloco
            │     └── IfElse
            │           ├── "if"
            │           ├── "("
            │           ├── Condicao
            │           ├── ")"
            │           ├── "{"
            │           ├── Bloco
            │           │     └── ε
            │           ├── "}"
            │           ├── "else"
            │           ├── "{"
            │           ├── Bloco
            │           │     └── If
            │           │           ├── "if"
            │           │           ├── "("
            │           │           ├── Condicao
            │           │           ├── ")"
            │           │           ├── "{"
            │           │           ├── Bloco
            │           │           │     └── ε
            │           │           └── "}"
            │           └── "}"
            ├── "}"
            ├── "else"
            ├── "{"
            ├── Bloco
            │     └── IfElse
            │           ├── "if"
            │           ├── "("
            │           ├── Condicao
            │           ├── ")"
            │           ├── "{"
            │           ├── Bloco
            │           │     └── ε
            │           ├── "}"
            │           ├── "else"
            │           ├── "{"
            │           ├── Bloco
            │           │     └── ε
            │           └── "}"
            └── "}"


