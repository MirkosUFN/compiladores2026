Conforme a sintaxe para a linguagem C (simplificada) para o IF, abaixo

SIF -> PR:IF [AP][CONDICAO][FP][ACH][BLOCO][FCH]
CONDICAO -> [NOMEVAR][COMPARACAO][NOMEVAR]|[NOMEVAR][COMPARACAO][VALOR]|PR:TRUE
COMPARACAO -> > | < | >= | <= | == | !=
BLOCO -> ... | SIF
VALOR -> INTEIRO | FRACIONARIO

Construa a árvore de derivação para:

if(x>0){
  if(y>0){
    w=10;
    }
}
