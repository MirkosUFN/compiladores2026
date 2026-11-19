int main(void) {
    int dados[3] = {8, 6, 10};
    double media = (dados[0] + dados[1] + dados[2]) / 3.0;
    char conceito = 'B';
    if (media >= 7.0 && conceito == 'B') {
        /* Os delimitadores neste comentário [({ são ignorados. */
        return 0;
    }
    return 1;
}
