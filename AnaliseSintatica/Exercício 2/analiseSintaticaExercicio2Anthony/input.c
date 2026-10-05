int numero = 10;
int vetor[5] = {1, 2, 3, 4, 5};
float matriz[2][2];
int total = (numero + (vetor[0] * 2));

void processar(int limite) {
    if (total > limite) {
        matriz[0][1] = (total / 2.0);
    }
}
