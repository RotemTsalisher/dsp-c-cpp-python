#include <stdio.h>

#define MAX_R_SIZE 100

void process_residual(double x[], double t[], int size);
inline double sum_kahan(double x[], int size);

int main(void)
{
    double x[] = {1.0, 2.11, 3.0, 4.0};
    double t[] = {3.124, 1.0, 1.5, 2.0};

    int size = sizeof(x) / sizeof(x[0]);

    process_residual(x, t, size);

    return 0;
};

void process_residual(double x[], double t[], int size) {
    
    double g = 0.0;
    double r[MAX_R_SIZE] = {0.0};
    double r_squared[MAX_R_SIZE] = {0.0};
    double e_r = 0.0;

    double t_ = sum_kahan(t, size);
    double x_ = sum_kahan(x, size);

    double tt = t_ * t_;
    double tx = t_ * x_;

    g = (tt == 0.0 ? 0.0 : (tx / tt));

    for(int i = 0; i < size; ++i) {
        r[i] = x[i] - g * t[i];
        r_squared[i] = r[i] * r[i];
    };

    e_r = sum_kahan(r_squared, size);

    printf("\n=== process_residual ===\n");
    printf("sum(t)      = %lf\n", t_);
    printf("sum(x)      = %lf\n", x_);
    printf("t^2         = %lf\n", tt);
    printf("t*x         = %lf\n", tx);
    printf("gain (g)    = %lf\n", g);
    printf("energy(r)   = %lf\n", e_r);
};

inline double sum_kahan(double x[], int size) {
    double sum = 0.0, c = 0.0;
    double t,y;

    for(int i = 0; i < size; ++i) {
        y = x[i] - c;
        t = sum + y;

        c = (t - sum) - y;
        sum = t;
    };

    return sum;
};