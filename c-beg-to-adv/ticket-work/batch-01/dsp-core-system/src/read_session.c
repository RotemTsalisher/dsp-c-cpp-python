#include "dsp/read_session.h"

#include <stdio.h>

int parse_gain_db_text(char const* const text, double* const gain_db_out)
{
    if (text == 0 || gain_db_out == 0) {
        return 0;
    }
    return sscanf(text, "%d", (int*)gain_db_out);
}
