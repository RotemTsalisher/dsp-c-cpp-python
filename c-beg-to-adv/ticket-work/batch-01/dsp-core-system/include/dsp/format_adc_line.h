#ifndef DSP_FORMAT_ADC_LINE_H
#define DSP_FORMAT_ADC_LINE_H

#include <stddef.h>

int format_adc_line(char* buf, size_t buf_size, int counts, double volts);

#endif
