int notas[4] = {7, 8, 5, 10};
int matriz[2][2] = {{1, 2}, {3, 4}};
int soma = 0;
for (int i = 0; i < 4; i++) {
    if ((notas[i] > 6) && (i != 0)) {
        soma = soma + notas[i];
    }
}
float media = (soma * 1.0) / (4 - 1);
