#include <stdio.h>
#include <stdlib.h>

#define PSD_BINS_SIZE 16

double find_peak(const double *arr, int size);

static double psd_bins[PSD_BINS_SIZE];

int main() {

    int bin_count = 0;
    printf("Enter amount of bins [1 - 16] : ");
    scanf("%d", &bin_count);

    for(int i = 0; i < bin_count; ++i) {
        printf("Enter value for bin [%d] : ", i + 1);
        scanf("%lf", psd_bins + i);
    };

    printf("Peak bin = %5.3lf\n", find_peak(psd_bins, bin_count));
    return 0;
};

double find_peak(const double *arr, int size) {
    double peak = arr[0];

    for(int i = 1; i < size; ++i){
        if(arr[i] > peak) {
            peak = arr[i];
        }
    };

    return peak;
};