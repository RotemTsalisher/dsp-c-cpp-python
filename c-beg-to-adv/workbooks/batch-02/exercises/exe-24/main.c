#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double counts_to_volts(int c, int bits, double vref);
double volts_to_dbfs(double v, double vref);
int led_level(double dbfs);

int main()
{
    int counts[] = { 20, 80, 1200, 3200 };
    int bits = 12;
    double vref = 3.3;

    for (int i = 0; i < 4; i++)
    {
        double v = counts_to_volts(counts[i], bits, vref);
        double dbfs = volts_to_dbfs(v, vref);
        int led = led_level(dbfs);

        printf("counts=%4d  V=%.3f  dBFS=%.1f  LED=%d\n",
               counts[i], v, dbfs, led);
    }

    return 0;
}

double counts_to_volts(int c, int bits, double vref) {
    return (c / (powf(2, bits) - 1.0) ) * vref;
}

double volts_to_dbfs(double v, double vref) {
    return 20.0 * logf(v / vref);
}

int led_level(double dbfs) {
    if (dbfs < -40.0) {
        return 0;
    }

    if (dbfs < -20.0) {
        return 1;
    }

    if(dbfs < -6.0) {
        return 2;
    }

    return 3;
};