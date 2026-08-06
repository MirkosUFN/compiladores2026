#include <stdio.h>

// Função
int somar(int a, int b) {
    return a + b;
}

// Struct
struct Pessoa {
    char nome[50];
    int idade;
    float altura;
};

int main() {

    // ==========================
    // Declaração de variáveis
    // ==========================
    int idade, opcao;
    int a = 10, b = 3;
    float altura;
    double preco = 99.99;
    char letra;
    char nome[50];

    // ==========================
    // printf() e scanf()
    // ==========================
    printf("Digite seu nome: ");
    scanf("%49s", nome);

    printf("Digite sua idade: ");
    scanf("%d", &idade);

    printf("Digite sua altura: ");
    scanf("%f", &altura);

    printf("Digite uma letra: ");
    scanf(" %c", &letra);

    printf("\n--- Dados Informados ---\n");
    printf("Nome: %s\n", nome);
    printf("Idade: %d\n", idade);
    printf("Altura: %.2f\n", altura);
    printf("Letra: %c\n", letra);
    printf("Preco: %.2lf\n", preco);

    // ==========================
    // Operadores
    // ==========================
    printf("\n--- Operadores ---\n");
    printf("%d + %d = %d\n", a, b, a + b);
    printf("%d - %d = %d\n", a, b, a - b);
    printf("%d * %d = %d\n", a, b, a * b);
    printf("%d / %d = %d\n", a, b, a / b);
    printf("%d %% %d = %d\n", a, b, a % b);

    // ==========================
    // if / else
    // ==========================
    printf("\n--- if / else ---\n");
    if (idade >= 18) {
        printf("Maior de idade.\n");
    } else {
        printf("Menor de idade.\n");
    }

    // ==========================
    // else if
    // ==========================
    printf("\n--- else if ---\n");
    if (idade >= 60) {
        printf("Idoso.\n");
    } else if (idade >= 18) {
        printf("Adulto.\n");
    } else {
        printf("Crianca/Adolescente.\n");
    }

    // ==========================
    // switch
    // ==========================
    printf("\n--- Switch ---\n");
    printf("Escolha uma opcao (1 ou 2): ");
    scanf("%d", &opcao);

    switch (opcao) {
        case 1:
            printf("Iniciar\n");
            break;
        case 2:
            printf("Configuracoes\n");
            break;
        default:
            printf("Opcao invalida\n");
    }

    // ==========================
    // for
    // ==========================
    printf("\n--- For ---\n");
    for (int i = 0; i < 5; i++) {
        printf("%d ", i);
    }

    // ==========================
    // while
    // ==========================
    printf("\n\n--- While ---\n");
    int x = 0;
    while (x < 5) {
        printf("%d ", x);
        x++;
    }

    // ==========================
    // do while
    // ==========================
    printf("\n\n--- Do While ---\n");
    int num;
    do {
        printf("Digite 0 para sair: ");
        scanf("%d", &num);
    } while (num != 0);

    // ==========================
    // Vetor
    // ==========================
    printf("\n--- Vetor ---\n");
    int numeros[5] = {10, 20, 30, 40, 50};

    for (int i = 0; i < 5; i++) {
        printf("%d ", numeros[i]);
    }

    // ==========================
    // Função
    // ==========================
    printf("\n\n--- Funcao ---\n");
    int resultado = somar(5, 8);
    printf("5 + 8 = %d\n", resultado);

    // ==========================
    // Ponteiro
    // ==========================
    printf("\n--- Ponteiro ---\n");
    int valor = 100;
    int *p = &valor;

    printf("Valor: %d\n", *p);
    printf("Endereco: %p\n", (void *)p);

    // ==========================
    // Struct
    // ==========================
    printf("\n--- Struct ---\n");
    struct Pessoa pessoa;

    pessoa.idade = idade;
    pessoa.altura = altura;

    // Copiando o nome para a struct
    int i = 0;
    while (nome[i] != '\0') {
        pessoa.nome[i] = nome[i];
        i++;
    }
    pessoa.nome[i] = '\0';

    printf("Nome: %s\n", pessoa.nome);
    printf("Idade: %d\n", pessoa.idade);
    printf("Altura: %.2f\n", pessoa.altura);

    // ==========================
    // Arquivos
    // ==========================
    printf("\n--- Arquivos ---\n");

    FILE *f = fopen("dados.txt", "w");

    if (f != NULL) {
        fprintf(f, "Nome: %s\n", pessoa.nome);
        fprintf(f, "Idade: %d\n", pessoa.idade);
        fprintf(f, "Altura: %.2f\n", pessoa.altura);
        fclose(f);
        printf("Dados gravados em dados.txt\n");
    } else {
        printf("Erro ao criar arquivo.\n");
    }

    f = fopen("dados.txt", "r");

    if (f != NULL) {
        char texto[100];

        printf("\nConteudo do arquivo:\n");
        while (fgets(texto, sizeof(texto), f) != NULL) {
            printf("%s", texto);
        }

        fclose(f);
    } else {
        printf("Erro ao abrir arquivo.\n");
    }

    return 0;
}
