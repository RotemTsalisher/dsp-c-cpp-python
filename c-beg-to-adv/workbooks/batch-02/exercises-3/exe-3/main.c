#include <stdio.h>
#include <stdlib.h>

#define SUB   "SUB"
#define BASS  "BASS"
#define MID   "MID"
#define HIGH  "HIGH"
#define OTHER "OOB"

#define INT_IN_INCLUSIVE_RANGE(v,a,b)   (v >= a && v <= b)
#define PRINT_LINE_FMT                  "Index : %d | Label : %s | Level : %d\n"

const char *band_label(int bin_index);
int energy_level(double power, double ref);

int main(void)
{
    double ref = 100.0;

    int bins[] = {0, 3, 7, 12, 20};
    double powers[] = {20.0, 40.0, 60.0, 80.0, 120.0};

    for (int i = 0; i < 5; ++i) {
        printf(
            PRINT_LINE_FMT,
            bins[i],
            band_label(bins[i]),
            energy_level(powers[i], ref)
        );
    }

    return 0;
}

const char *band_label(int bin_index) {
    if(INT_IN_INCLUSIVE_RANGE(bin_index, 0, 1)) {
        return SUB;
    }
    else if (INT_IN_INCLUSIVE_RANGE(bin_index, 2, 5)) {
        return BASS;
    }
    else if (INT_IN_INCLUSIVE_RANGE(bin_index, 6, 9)) {
        return MID;
    }
    else if (INT_IN_INCLUSIVE_RANGE(bin_index, 10, 15)) {
        return HIGH;
    }
    else {
        return OTHER;
    }
}

int energy_level(double power, double ref) {
    double ratio = power / ref;

    if(ratio <= 0.25) {
        return 0;
    }
    else if (ratio <= 0.5) {
        return 1;
    }
    else if (ratio < 0.75) {
        return 2;
    }
    else {
        return 3;
    }
}