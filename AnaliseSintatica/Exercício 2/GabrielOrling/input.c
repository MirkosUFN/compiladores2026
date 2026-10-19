#include <stdio.h>

int main() {
    int v[5] = {1, 2, 3, 4, 5};
    float media = 0.0;
    int i;

    for (i = 0; i < 5; i++) {
        if ((v[i] % 2) == 0) {
            media = media + v[i];
        }
    }

    printf("Media: %f\n", media / 5.0);
    return 0;
}
