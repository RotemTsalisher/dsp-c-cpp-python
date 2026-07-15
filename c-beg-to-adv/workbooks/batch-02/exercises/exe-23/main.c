#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double mono_mix(double l, double r);
double to_db(double amp);


int main()
{
    double left  = 0.8;
    double right = 0.4;

    double mono = mono_mix(left, right);
    double db   = to_db(mono);

    printf("L     = %.3f\n", left);
    printf("R     = %.3f\n", right);
    printf("Mono  = %.3f\n", mono);
    printf("dB    = %.3f\n", db);

    return 0;
}


double mono_mix(double l, double r) {
    return 0.5f * (l + r);
}
double to_db(double amp) {
    if (amp > 0.0) {
        return 20.0 * logf(amp);
    }
    return -120.0;
}