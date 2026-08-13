#include <stdio.h>

#define TINY                         1e-16
#define PRINT_FMT                    "sum : %lf || y : %lf || t : %lf || c : %lf\n"
#define PRINT_RES(sum_, y_, t_, c_)  printf(PRINT_FMT, sum_, y_, t_, c_)  

void sum_and_compensate(double sum, double y);

int main() {

    sum_and_compensate(1.0, TINY);
    return 0;
};

void sum_and_compensate(double sum, double y) {
    double t = sum + y;
    double c = (t - sum) - y;

    PRINT_RES(sum,y, t, c);
};
