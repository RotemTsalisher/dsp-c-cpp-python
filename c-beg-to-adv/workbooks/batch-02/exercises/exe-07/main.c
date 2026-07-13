#include <stdio.h>
#include <stdlib.h>

#define PWR_TO_PCT 100.0
#define HEADER_ "BIN POWER PCT\n"
#define MESSEGE_FMT "BIN %d : PWR = %5.3f || PCT = %5.3f\n" 

int main() {

    double bin_7_pwr = 0.031, bin_8_pwr = 0.12, bin_9_pwr = 0.449;
    printf(HEADER_);
    printf(MESSEGE_FMT, 7, bin_7_pwr, bin_7_pwr * PWR_TO_PCT);
    printf(MESSEGE_FMT, 8, bin_8_pwr, bin_8_pwr * PWR_TO_PCT);
    printf(MESSEGE_FMT, 9, bin_9_pwr, bin_9_pwr * PWR_TO_PCT);
    return 0;
}