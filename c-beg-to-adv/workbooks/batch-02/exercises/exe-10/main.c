#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define MAG(x) (x > 0 ? x : -x)

int main() {

    double L = .73, R = -0.41;
    double mono_mix = 0.5 * (L + R);
    double peak_mag = (MAG(L) > MAG(R) ? MAG(L) : MAG(R));

    double headroom_db = 20.0 * log10f( 1.0 / peak_mag );

    printf("mono mix = %5.3f | peak mag = %5.3f | headroom [dB] = %5.3f |\n", mono_mix, peak_mag, headroom_db);
    return 0;
}