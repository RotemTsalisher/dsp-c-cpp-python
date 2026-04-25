#ifndef __STRUCTS__H
#define __STRUCTS__H
#include <cmath>


struct ComplexSample {
    double re,im;
    double (*mag)(const ComplexSample* c);
};

double magnitude(const ComplexSample* c) {
    return std::sqrt(c->re * c->re + c->im * c->im);
};

void ComplexSampleInit(ComplexSample* c) {
    c->re = 0;
    c->im = 0;
    c->mag = magnitude;
};

void ComplexSampleInit(ComplexSample* c, double re_, double im_){
    c->re = re_;
    c->im = im_;
    c->mag = magnitude;
};
#endif