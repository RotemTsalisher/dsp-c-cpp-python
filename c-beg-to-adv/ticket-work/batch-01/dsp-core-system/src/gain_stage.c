#include "dsp/gain_stage.h"

#include <math.h>

void gain_stage_init(GainStage* const stage)
{
    if (stage != 0) {
        stage->linear = 1.0;
    }
}

void gain_stage_set_db(GainStage* const stage, double const db)
{
    (void)stage;
    (void)db;
}

double gain_stage_linear(GainStage const* const stage)
{
    if (stage == 0) {
        return 0.0;
    }
    return stage->linear;
}
