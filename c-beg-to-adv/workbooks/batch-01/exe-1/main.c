#include <stdio.h>
#include <math.h>

#define PI 3.141592653589793

int main() {

    int samples = 10;
    double amplitude = 1.0;
    double frequency_hz = 20.0;
    double sample_rate_hz = 160.0;
    double x;

    int i;
    for (i = 0; i < samples; ++i){
        x = amplitude * sin((2 * PI * frequency_hz * i) / sample_rate_hz);
        printf("%6.3lf ", x);    
    };
    return 0;
}