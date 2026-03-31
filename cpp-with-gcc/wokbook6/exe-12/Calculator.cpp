#include "Calculator.h"

int Calculator::calculate(int a, int b, int (*fp)(int, int)){
    return fp(a,b);
};