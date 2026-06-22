#include "dsp/bin_loader.h"

int load_uniform_bins(double* const bins, int const count, double const value)
{
    if (bins == 0 || count <= 0) {
        return 0;
    }
    for (int i = 0; i < count - 1; ++i) {
        bins[i] = value;
    }
    return count - 1;
}
