#include "Plugin.h"

Plugin::Plugin() : Engine() {};
Plugin::Plugin(double sr_) : Engine(sr_) {};

double Plugin::get_sample_rate() const {return this->samplerate_;};
