#define THEIRS

#ifdef MINE
#include <stdio.h>
#include <stdlib.h>

void process_residual(const double *t, const double *x, int n,double *r,double *g, double *energy);

int main(void)
{

    printf("\nMINE!\n\n");
    double t[8] = {1,1,1,1,0,0,0,0};
    double x[8] = {2,2,2,2,1,1,1,1};
    double r[8];
    double g, energy;
    process_residual(t, x, 8, r, &g, &energy);
    printf("g=%.6f energy=%.6f\n", g, energy);
    for (int i = 0; i < 8; ++i) printf("%.4f ", r[i]);
    putchar('\n');
    return 0;
}

void process_residual(const double *t, const double *x, int n,double *r,double *g, double *energy) {

    double tt = 0.0, tx = 0.0;

    for(int i = 0; i < n; ++i) {
        tt += (t[i] * t[i]);
        tx += (t[i] * x[i]);
    };

    *g = (tt == 0) ? 0.0 : (tx / tt);

    *energy = 0.0;
    double c = 0.0;
    for(int i = 0; i < n; ++i) {
        r[i] = x[i] - (*g)*t[i];

        double y = r[i]*r[i] - c;
        double sum = *energy + y;

        c = (sum - *energy) - y;
        *energy = sum;
    }
}

#else
#include <stdio.h>

void process_residual(double const *t, double const *x, int n,
                      double *r, double *g_out, double *energy_out)
{
    double tt = 0.0, tx = 0.0;
    for (int i = 0; i < n; ++i) {
        tt += t[i] * t[i];
        tx += t[i] * x[i];
    }
    double g = (tt == 0.0) ? 0.0 : (tx / tt);
    double energy = 0.0;
    double c = 0.0; /* Kahan compensation */
    for (int i = 0; i < n; ++i) {
        r[i] = x[i] - g * t[i];
        double const y = r[i] * r[i] - c;
        double const sum = energy + y;
        c = (sum - energy) - y;
        energy = sum;
    }
    *g_out = g;
    *energy_out = energy;
}

int main(void)
{
    printf("\nTHEIRS!\n\n");
    double t[8] = {1,1,1,1,0,0,0,0};
    double x[8] = {2,2,2,2,1,1,1,1};
    double r[8];
    double g, energy;
    process_residual(t, x, 8, r, &g, &energy);
    printf("g=%.6f energy=%.6f\n", g, energy);
    for (int i = 0; i < 8; ++i) printf("%.4f ", r[i]);
    putchar('\n');
    return 0;
}

#endif