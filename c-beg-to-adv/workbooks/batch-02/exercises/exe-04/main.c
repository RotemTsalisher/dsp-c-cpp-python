#include <stdio.h>
#include <stdlib.h>

double abs_(double sample);

static double samples[5] = {0.2, -0.5, 0.5, 0.5, -0.1};

int main() {

    int frame_count = 0;
    double energy_sum = 0.0;
    double peak = 0.0;
    double abs_sample;

    for(int i = 0; i < 5; ++i) {
        abs_sample = abs_(samples[i]);
        energy_sum += (samples[i] * samples[i]);
        if(abs_sample > peak) {
            peak = abs_sample;
        };
    };

    printf("Frames %d | Energy Sum = %.4lf | Peak = %.4lf\n", 5, energy_sum, peak);

    return 0;
}

double abs_(double sample) {
    if(sample < 0.0) {
        return -sample;
    };
    return sample;
};