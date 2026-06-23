#include <stdio.h>

const double b0 = 0.02,b1 = 0.05,b2 = 0.11,b3 = 0.40,b4 = 0.22,b5 = 0.08,b6 = 0.03,b7 = 0.01;

int main() {

    double max_pow = b0 ;

    if(b1  > max_pow) {
        max_pow = b1;
    }
    if(b2  > max_pow) {
        max_pow = b2;
    }
    if(b3  > max_pow) {
        max_pow = b3;
    }
    if(b4  > max_pow) {
        max_pow = b4;
    }
    if(b5  > max_pow) {
        max_pow = b5;
    }
    if(b6  > max_pow) {
        max_pow = b6;
    }
    if(b7  > max_pow) {
        max_pow = b7;
    }

    printf("bin %d | %5.3f | *\n", 0, b0);
    printf("bin %d | %5.3f | *\n", 1, b1);
    printf("bin %d | %5.3f | *\n", 2, b2);
    printf("bin %d | %5.3f | *\n", 3, b3);
    printf("bin %d | %5.3f | *\n", 4, b4);
    printf("bin %d | %5.3f | *\n", 5, b5);
    printf("bin %d | %5.3f | *\n", 6, b6);
    printf("bin %d | %5.3f | *\n", 7, b7);

    printf("max pow = %5.3f\n", max_pow);
    return 0;
}
