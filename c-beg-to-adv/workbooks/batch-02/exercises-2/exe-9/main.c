#include <stdio.h>
#include <stdlib.h>

#define N 8
#define PRINT_FMT "ID : %d | Power : %4.2lf |\n"

struct Frame {
    int id;
    float power;
};

int id_of_max_power(const double *power_array, const int *id_array, int size);

int main() {

    int id_array[N] = {0};
    double power_array[N] = {0.0};

    int n = -1;
    struct Frame tmp;

    printf("Enter n [1 - 8] : ");
    scanf(" %d", &n);

    for(int i = 0; i < n; ++i) {
        printf("Enter ID, Power Pair : ");
        scanf("%d %lf", id_array + i, power_array + i);
    };

    printf("====== ID, Power Pairs: =====\n");

    for(int i = 0; i < n; ++i) {
        printf(PRINT_FMT, id_array[i], power_array[i]);
    }
    printf("ID of Max Power : %d\n", id_of_max_power(power_array, id_array, n));
    return 0;
}

int id_of_max_power(const double *power_array, const int *id_array, int size) {
    double power_tmp = power_array[0];
    int    id_tmp    = id_array[0];
    for(int i = 1; i < size; ++i) {
        printf("INSIDE MAX PWR : ID %d, Power %4.2lf\n", id_array[i], power_array[i]);
        if(power_array[i] > power_tmp) {
            power_tmp = power_array[i];
            id_tmp = id_array[i];
        }
    }

    return id_tmp;
};