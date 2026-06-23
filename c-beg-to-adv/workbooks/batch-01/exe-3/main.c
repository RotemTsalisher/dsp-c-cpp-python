#include <stdio.h>
#include <math.h>
#define INF 100000000.0
int main() {
    double left = 0.0 ,right = -0.0;

    double mono = 0.5 * (left + right);
    double quad_energy = 0.5 * (left * left + right * right);
    double db10 = quad_energy > 0.0 ? 10.0 * log10(quad_energy) : -INF;
    
    printf("mono = %6.3f\n", mono);
    printf("quad_energy = %6.3f\n", quad_energy);

    if(db10 != -INF) {
        printf("db10 = %6.3f\n", db10);
    }
    else {
        printf("db10 = -inf\n");
    }

    return 0;
}