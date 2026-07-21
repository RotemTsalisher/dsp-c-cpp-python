#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>



#define SIZE 6


static double buffer_a[SIZE] = {
    1.0, 2.0, 3.0, 4.0, 5.0, 6.0
};

static double buffer_b[SIZE] = {
    10.0, 20.0, 30.0, 40.0, 50.0, 60.0
};
  
void print_vector(const double *v, int size);

int main() {

    double scaled[SIZE];
    double mix[SIZE];

    for(int i = 0; i < SIZE; ++i) {
        scaled[i] = 0.5 * buffer_a[i];
        mix[i] = scaled[i] + buffer_b[i];
    };

    printf("SCALED BUFFER : ");
    print_vector(scaled, SIZE);

    printf("MIX BUFFER : ");
    print_vector(mix, SIZE);

    return 0;
};

void print_vector(const double *v, int size) {
    printf("<");
    for(int i = 0; i < size - 1; ++i) {
        printf("%4.2lf,",v[i]);
    };
    printf("%4.2lf>\n", v[size-1]);
};