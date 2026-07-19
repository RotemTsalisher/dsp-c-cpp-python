#include <stdio.h>
#include <stdlib.h>

#define PRINT_MSG "band %c | fft %d | tier %d\n"

int main() {

    char band = '?';
    int fft_size = 0;

    printf("Enter Band ['A' - 'D'] : ");
    scanf(" %c", &band);

    switch(band) {
        case 'A':
        case 'B':
            fft_size = 256;
            break;
        case 'C':
            fft_size = 512;
            break;
        case 'D':
            fft_size = 1024;
            break;
    }

    printf(PRINT_MSG, band, fft_size, (int)(band - 'A' + 1));
    return 0;
}