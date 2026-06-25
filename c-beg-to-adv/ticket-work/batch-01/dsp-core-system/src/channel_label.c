#include "dsp/channel_label.h"

#include <string.h>

int channel_label_is_uplink(char const label[DSP_LABEL_MAX])
{
    if (label == 0) {
        return 0;
    }
    return strcmp(label, "uplink\n") == 0;
}
