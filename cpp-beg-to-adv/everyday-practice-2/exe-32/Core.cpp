#include "Core.h"

Core::Core() : fftOrder_(512) {};
Core::Core(int fftOrder) : fftOrder_(fftOrder) {};
Core::Core(const Core& other) : fftOrder_(other.fftOrder_) {};

