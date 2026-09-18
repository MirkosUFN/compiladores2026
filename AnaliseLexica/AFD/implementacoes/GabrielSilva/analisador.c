#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define MAX_ESTADOS 100
#define MAX_SIMBOLOS 128
#define MAX_TRANSICOES 500
#define MAX_STR 50
#define MAX_LINHA 2048

typedef struct { char origem[MAX_STR]; char simbolo; char destino[MAX_STR]; } Transicao;
typedef struct { char estado[MAX_STR]; char token[MAX_STR]; } EstadoFinal;
typedef struct {
    char estado_inicial[MAX_STR];
    char simbolos[MAX_SIMBOLOS];
    int num_simbolos;
    EstadoFinal estados_finais[MAX_ESTADOS];
    int num_estados_finais;
    Transicao transicoes[MAX_TRANSICOES];
    int num_transicoes;
} AFD;

bool pertence_alfabeto(AFD *afd, char c) {
    for (int i = 0; i < afd->num_simbolos; i++) {
        if (afd->simbolos[i] == c) return true;
    }
    return false;
}

void carregar_afd(const char *caminho, AFD *afd) {
    FILE *f = fopen(caminho, "r");
    if (!f) {
        printf("Erro: Arquivo %s nao encontrado.\n", caminho);
        exit(1);
    }
    char linha[MAX_LINHA];
    
    if(fgets(linha, sizeof(linha), f)) {
        char *tok = strtok(linha, " \t\r\n");
        if(tok) strcpy(afd->estado_inicial, tok);
    }
    
    afd->num_simbolos = 0;
    if(fgets(linha, sizeof(linha), f)) {
        char *tok = strtok(linha, " \t\r\n");
        while(tok) { afd->simbolos[afd->num_simbolos++] = tok[0]; tok = strtok(NULL, " \t\r\n"); }
    }
    
    afd->num_estados_finais = 0;
    if(fgets(linha, sizeof(linha), f)) {
        char *tok = strtok(linha, " \t\r\n");
        while(tok) {
            char *sep = strchr(tok, ':');
            if(sep) {
                *sep = '\0';
                strcpy(afd->estados_finais[afd->num_estados_finais].estado, tok);
                strcpy(afd->estados_finais[afd->num_estados_finais].token, sep + 1);
                afd->num_estados_finais++;
            }
            tok = strtok(NULL, " \t\r\n");
        }
    }
    
    afd->num_transicoes = 0;
    while(fgets(linha, sizeof(linha), f)) {
        char *tok = strtok(linha, " \t\r\n");
        while(tok) {
            char orig[MAX_STR], dest[MAX_STR], sim;
            if(sscanf(tok, "%[^:]:%c:%s", orig, &sim, dest) == 3) {
                strcpy(afd->transicoes[afd->num_transicoes].origem, orig);
                afd->transicoes[afd->num_transicoes].simbolo = sim;
                strcpy(afd->transicoes[afd->num_transicoes].destino, dest);
                afd->num_transicoes++;
            }
            tok = strtok(NULL, " \t\r\n");
        }
    }
    fclose(f);
}

void processar_palavra(AFD *afd, char *palavra, char *resultado_tipo) {
    char estado_atual[MAX_STR];
    strcpy(estado_atual, afd->estado_inicial);
    
    for(int i = 0; palavra[i] != '\0'; i++) {
        char c = palavra[i];
        if(!pertence_alfabeto(afd, c)) {
            strcpy(resultado_tipo, "ERRO_SIMBOLO");
            return;
        }
        bool mudou = false;
        for(int j = 0; j < afd->num_transicoes; j++) {
            if(strcmp(afd->transicoes[j].origem, estado_atual) == 0 && afd->transicoes[j].simbolo == c) {
                strcpy(estado_atual, afd->transicoes[j].destino);
                mudou = true;
                break;
            }
        }
        if(!mudou) {
            strcpy(resultado_tipo, "ERRO_TRANSICAO");
            return;
        }
    }
    
    for(int i = 0; i < afd->num_estados_finais; i++) {
        if(strcmp(afd->estados_finais[i].estado, estado_atual) == 0) {
            strcpy(resultado_tipo, afd->estados_finais[i].token);
            return;
        }
    }
    strcpy(resultado_tipo, "ERRO_ESTADO_NAO_FINAL");
}

int main() {
    AFD afd;
    carregar_afd("configAfd.md", &afd);
    
    FILE *f_in = fopen("input.c", "r");
    if(!f_in) {
        printf("Erro: Arquivo input.c nao encontrado.\n");
        return 1;
    }
    
    char linha[MAX_LINHA];
    int num_linha = 1;
    int id_token = 1;
    
    printf("%-5s | %-15s | %-20s | %-7s | %-7s\n", "ID", "TOKEN", "TIPO", "LINHA", "COLUNA");
    printf("-----------------------------------------------------------------\n");
    
    while(fgets(linha, sizeof(linha), f_in)) {
        char copia_linha[MAX_LINHA];
        strcpy(copia_linha, linha);
        
        int offset = 0;
        char *palavra = strtok(copia_linha, " \t\r\n");
        
        while(palavra) {
            // strstr encontra onde a palavra começou na linha original para calcular a coluna
            char *ptr = strstr(linha + offset, palavra);
            int coluna = (ptr - linha) + 1;
            offset = (ptr - linha) + strlen(palavra);
            
            char tipo_token[MAX_STR];
            processar_palavra(&afd, palavra, tipo_token);
            
            printf("%-5d | %-15s | %-20s | %-7d | %-7d\n", id_token, palavra, tipo_token, num_linha, coluna);
            
            id_token++;
            palavra = strtok(NULL, " \t\r\n");
        }
        num_linha++;
    }
    
    fclose(f_in);
    return 0;
}