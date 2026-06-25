#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define DELAY_RING_SIZE 8
#define INF 1000000000

void print_ring(const double *buffer, int size);
double ring_energy(const double *buffer, int size);

static double delay_ring[DELAY_RING_SIZE] = {
    0.0, 0.125, 0.250, 0.375, 0.500, 0.375, 0.250, 0.125
};

int main(){

    double ring_energy_ = ring_energy(delay_ring, DELAY_RING_SIZE);
    double ring_energy_dB = (ring_energy_ > 0) ? 10*log10(ring_energy_) : -INF;

    print_ring(delay_ring, DELAY_RING_SIZE);
    
    if(ring_energy_ > 0) {
        printf("Ring energy [dB] : %5.3lf\n", ring_energy_dB);
    }
    else {
        printf("Ring energy [dB] : -inf\n");
    }
    
    return 0;
}

void print_ring(const double *buffer, int size) {
    int i;

    for(i = 0; i<size; ++i){
        printf("[%d] : %8.4f\n",i, buffer[i]);
    };
};

double ring_energy(const double *buffer, int size) {
    double res = 0.0;

    int i;
    for(i = 0; i < size; ++i) {
        res += (buffer[i] * buffer[i]);
    }

    res /= size;
    return res;
};