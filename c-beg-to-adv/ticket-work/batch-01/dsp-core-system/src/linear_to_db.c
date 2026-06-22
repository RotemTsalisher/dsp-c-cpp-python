#include "dsp/linear_to_db.h"

#include <math.h>

double linear_power_to_db(double const linear_power)
{
    if (linear_power <= 0.0) {
        return 0.0;
    }
    return 20.0 * log10(linear_power);
}
