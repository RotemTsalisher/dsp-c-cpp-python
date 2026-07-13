#include <stdio.h>
#include <stdlib.h>

#define LINE1 "CERT | SN=%08d | REV=%c%c\n"
#define LINE2 "LIMIT | clip=%.4f | nominal=%.4f\n"
#define LINE4 "PASS @ %02d:%02d:%02d\n"

int main() {

    printf(LINE1, 12004567, 'B', '3');
    printf(LINE2, 1.0000, 0.8913);
    printf("----------------------------------------\n");
    printf(LINE4, 14, 6, 3);

    return 0;
};