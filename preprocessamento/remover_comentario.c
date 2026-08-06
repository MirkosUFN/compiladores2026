#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void filtrar_comentarios(FILE *in, FILE *out) {
    // Estados: 0=Normal, 1=Leu '/', 2=ComentarioLinha(//), 3=ComentarioBloco(/*), 4=PossivelFimBloco(*)
    int Estado = 0; 
    int c;

    while ((c = fgetc(in)) != EOF) {
        switch (Estado) {
            
            case 0:
                if (c == '/') {
                    Estado = 1; 
                } else {
                    fputc(c, out);
                }
                break;

            case 1: 
                if (c == '/') {
                    Estado = 2; 
                } else if (c == '*') {
                    Estado = 3; 
                } else {
                    fputc('/', out);
                    fputc(c, out);
                    Estado = 0;
                }
                break;

            case 2: 
                if (c == '\n') {
                    fputc(c, out); 
                    Estado = 0;
                }
                break;

            case 3: 
                if (c == '*') {
                    Estado = 4; 
                } else if (c == '\n') {
                    fputc(c, out); 
                }
                break;

            case 4: 
                if (c == '/') {
                    fputc(' ', out); 
                    Estado = 0;      
                } else if (c == '\n') {
                    fputc(c, out);
                    Estado = 3;
                } else if (c != '*') {
                    Estado = 3; 
                }
                break;
        }
    }

    if (Estado == 1) {
        fputc('/', out);
    }
}

int main() {
    char caminho[150];

    printf("=== Processador Lexico: Remocao de Comentarios ===\n");
    printf("Digite o nome do arquivo fonte: ");
    
    if (fgets(caminho, sizeof(caminho), stdin)) {
        caminho[strcspn(caminho, "\r\n")] = '\0';
    }

    FILE *arquivo = fopen(caminho, "r");
    if (!arquivo) {
        fprintf(stderr, "\n[Erro] Nao foi possivel abrir o arquivo: %s\n", caminho);
        return EXIT_FAILURE; 
    } 

    printf("\n--- SAIDA SEM COMENTARIOS ---\n");
    filtrar_comentarios(arquivo, stdout);
    printf("\n-----------------------------\n");
    
    fclose(arquivo);
    return EXIT_SUCCESS;
}