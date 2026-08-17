#include <stdio.h>

#define ABS(x)  (x > 0 ? x : -x)

inline double sum_kahan(double x[], int size);
inline double sum_naive(double x[], int size);
double abs_diff(double naive, double kahan);

int main(void)
{
    double x1[1000];
    double x2[1000];

    /* Test A: all ones */
    for (int i = 0; i < 1000; ++i)
    {
        x1[i] = 1.0;
    }

    /* Test B: x[0] = 1e6, rest = 1e-6 */
    x2[0] = 1e6;
    for (int i = 1; i < 1000; ++i)
    {
        x2[i] = 1e-6;
    }

    double naive_a = sum_naive(x1, 1000);
    double kahan_a = sum_kahan(x1, 1000);

    double naive_b = sum_naive(x2, 1000);
    double kahan_b = sum_kahan(x2, 1000);

    printf("TEST A (all ones)\n");
    printf("ABS(naive - kahan) = %.20lf\n\n",
           abs_diff(naive_a, kahan_a));

    printf("TEST B (1e6 + 999*1e-6)\n");
    printf("ABS(naive - kahan) = %.20lf\n\n",
           abs_diff(naive_b, kahan_b));

    /* Interpretation:
       Kahan and naive are identical for Test A, while Kahan is more
       accurate in Test B because it compensates for the tiny increments
       added after a very large value. */

    return 0;
};

inline double sum_kahan(double x[], int size) {

    double sum = 0.0, c = 0.0;
    double y,t;

    for(int i = 0; i < size; ++i) {
        y = x[i] - c;
        t = sum + y;

        c = (t - sum) - y;
        sum = t;
    };

    return sum;
};

inline double sum_naive(double x[], int size) {
    double sum = 0.0;

    for(int i = 0; i < size; ++i) {
        sum += x[i];
    }
    return sum;
};

double abs_diff(double naive, double kahan) {
    return ABS((naive - kahan));
};