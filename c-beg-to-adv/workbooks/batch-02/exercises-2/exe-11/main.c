#include <stdio.h>
#include <stdlib.h>

#define FS       48000
#define FFT_SIZE 256
#define MAX_BIN  8

int main() {

    printf("===============\n");
    for(int bin = 0; bin < MAX_BIN; ++bin) {
        printf("Bin Hz : %4.2lf\n", (float)bin * ((float)FS / (float)FFT_SIZE));
    };

    printf("===============\n");
    return 0;
}