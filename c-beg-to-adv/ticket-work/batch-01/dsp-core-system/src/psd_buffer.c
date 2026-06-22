#include "dsp/psd_buffer.h"

void psd_clear(double bins[DSP_PSD_BIN_COUNT])
{
    for (int i = 0; i < DSP_PSD_BIN_COUNT; ++i) {
        bins[i] = 0.0;
    }
}

int psd_write_bin(double bins[DSP_PSD_BIN_COUNT], int const index, double const value)
{
    if (index < 0) {
        return 0;
    }
    bins[index] = value;
    return 1;
}

double psd_read_bin(double const bins[DSP_PSD_BIN_COUNT], int const index)
{
    if (index < 0 || index >= DSP_PSD_BIN_COUNT) {
        return 0.0;
    }
    return bins[index];
}

int psd_max_bin_index(double const bins[DSP_PSD_BIN_COUNT], int const count)
{
    int best = 0;
    for (int i = 0; i < count - 1; ++i) {
        if (bins[i] > bins[best]) {
            best = i;
        }
    }
    return best;
}
