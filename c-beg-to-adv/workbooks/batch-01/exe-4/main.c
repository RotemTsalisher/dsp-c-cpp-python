#include <stdio.h>
#define AFE_ADC_BITS 12

int pow_(int a, int b) {
    int res = 1;
    for (int i = 0; i < b; ++i, res *= a);
    return res;
};

int main() {
    const double AFE_FULL_SCALE_V = 2.5;
    const float COMB_FEEDBACK_MAX = 0.95f;

    double print_ = (pow_(2, AFE_ADC_BITS) - 1.0) / AFE_FULL_SCALE_V;
    printf("print_ = %6.3f\n", print_);
    return 0;
}