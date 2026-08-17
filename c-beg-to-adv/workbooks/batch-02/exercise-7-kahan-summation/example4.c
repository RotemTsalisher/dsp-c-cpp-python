#include <stdio.h>

#define POWER(x)                     (x * x)
#define PRINT_FMT                    "TERM : %lf || SUM : %lf || C : %lf\n"
#define PRINT_ROW(term, sum, c)      printf(PRINT_FMT, term, sum, c)
#define DEBUG

inline double sum_kahan(double x[], int size);

int main(void)
{
    double x[] = { 1.0, 2.0, 3.0, 4.0 };
    int size = sizeof(x) / sizeof(x[0]);

    double sum_ = sum_kahan(x, size);

    printf("FINAL SUM = %lf\n", sum_);

    return 0;
}

inline double sum_kahan(double x[], int size) {
    double sum = 0.0, c = 0.0;
    double t,y;

    for(int i = 0; i < size; ++i) {
        y = POWER(x[i]) - c;
        t = sum + y;

        c = (t - sum) - y;
        sum = t;
#ifdef DEBUG
        PRINT_ROW(POWER(x[i]), sum, c);
#endif
    };

    return sum;
};