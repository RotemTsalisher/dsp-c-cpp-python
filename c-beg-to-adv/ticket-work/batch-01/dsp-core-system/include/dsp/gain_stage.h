#ifndef DSP_GAIN_STAGE_H
#define DSP_GAIN_STAGE_H

typedef struct GainStage {
    double linear;
} GainStage;

void gain_stage_init(GainStage* stage);
void gain_stage_set_db(GainStage* stage, double db);
double gain_stage_linear(GainStage const* stage);

#endif
