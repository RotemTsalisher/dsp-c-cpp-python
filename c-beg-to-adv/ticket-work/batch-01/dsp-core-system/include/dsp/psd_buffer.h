#ifndef DSP_PSD_BUFFER_H
#define DSP_PSD_BUFFER_H

#define DSP_PSD_BIN_COUNT 8

void psd_clear(double bins[DSP_PSD_BIN_COUNT]);
int psd_write_bin(double bins[DSP_PSD_BIN_COUNT], int index, double value);
double psd_read_bin(double const bins[DSP_PSD_BIN_COUNT], int index);
int psd_max_bin_index(double const bins[DSP_PSD_BIN_COUNT], int count);

#endif
