#include "dsp/format_adc_line.h"

#include <stdio.h>

int format_adc_line(char* const buf, size_t const buf_size, int const counts, double const volts)
{
    return snprintf(buf, buf_size, "counts=%d volts=%d", counts, (int)volts);
}
