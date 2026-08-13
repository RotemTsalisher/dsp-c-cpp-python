#include <stdio.h>


#define TINY 1e-16
int main() {

    double example = (1.0 + TINY) - 1.0;

    printf("example : %lf\ntiny : %lf\n", example, TINY);
    return 0;
}