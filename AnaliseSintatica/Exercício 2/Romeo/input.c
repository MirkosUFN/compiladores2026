int notas[3] = {7, 8, 10};
int matriz[2][2] = {{1, 2}, {3, 4}};
float media = (notas[0] + notas[1]) / 2.0;

if (media >= 7.0) {
    if ((notas[2] > 9) && (media < 10)) {
        matriz[0][1] = 5;
    }
} else {
    media = ((media * 2) + 1);
}
