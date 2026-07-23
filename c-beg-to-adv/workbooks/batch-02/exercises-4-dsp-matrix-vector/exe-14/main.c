#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void energy_interleaved_buffer(const double *buffer, int single_channel_length, double *energy_l, double *energy_r) {
    *energy_l = 0.0;
    *energy_r = 0.0;
    
    for(int i = 0; i < 2*single_channel_length; i += 2) {
        *energy_l += (buffer[i] * buffer[i]);
        *energy_r += (buffer[i + 1] * buffer[i + 1]);
    }
};

void interleaved_buffer_to_mono(const double *interleaved_buffer, int single_channel_length, double *mono_buffer) {
    for(int i = 0; i < single_channel_length; i++) {
        mono_buffer[i] = 0.5 * (interleaved_buffer[2*i] + interleaved_buffer[2*i + 1]);
    };
};

int main(void) {

    const int N = 6;

    double interleaved[2 * N] = {
        1, 10,
        2, 20,
        3, 30,
        4, 40,
        5, 50,
        6, 60
    };

    double mono[N];
    double energy_l, energy_r;

    energy_interleaved_buffer(
        interleaved,
        N,
        &energy_l,
        &energy_r
    );

    interleaved_buffer_to_mono(
        interleaved,
        N,
        mono
    );

    printf("Interleaved:\n");
    for(int i = 0; i < 2 * N; i += 2) {
        printf("L=%5.1lf R=%5.1lf\n",
               interleaved[i],
               interleaved[i + 1]);
    }

    printf("\nEnergy L = %.1lf\n", energy_l);
    printf("Energy R = %.1lf\n", energy_r);

    printf("\nMono:\n");
    for(int i = 0; i < N; ++i) {
        printf("%.1lf ", mono[i]);
    }

    printf("\n");

    return 0;
}