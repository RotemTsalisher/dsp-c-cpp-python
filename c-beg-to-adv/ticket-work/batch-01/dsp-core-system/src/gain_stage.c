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
    stage->linear = pow(10, (db / 20.0)); 
}

double gain_stage_linear(GainStage const* const stage)
{
    if (stage == 0) {
        return 0.0;
    }
    return stage->linear;
}
