#ifndef DSP_APPLY_GAIN_FN_H
#define DSP_APPLY_GAIN_FN_H

typedef double (*GainFn)(double);

double apply_gain_fn(double sample, GainFn fn);

#endif
