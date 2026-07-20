#include <stdio.h>
#include <stdlib.h>


int main() {

    double l = 0.25, r = -0.5;
    printf("L : %4.2lf | R : %4.2lf | Mono Mix : %5.3lf\n", l, r, 0.5*(l + r));
    
    return 0;
}