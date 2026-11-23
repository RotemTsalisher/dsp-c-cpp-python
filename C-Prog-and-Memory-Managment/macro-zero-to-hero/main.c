#include "stdio.h"

#define PRINT_AND_DOUBLE(x) \
    printf("x = %d\n", (x)); \
    (x) *= 2;

#define INIT_VAR(T, name, val) \
    T name = val; 


#define INIT_VAR_IF(T, name, val, condition) \
    T name = (condition) ? val : 0;

#define ASSRT_OP(T, a, b, op) \
    do { \
        T _a = (a); \
        T _b = (b); \
        if(_a op _b) { \
            printf("PASS!\n"); \
        } \
        else { \
            printf("FAIL!\n"); \
        } \
    } while(0)

int main() {

    int z = 2;

    ASSRT_OP(int, z, 2, ==);
    ASSRT_OP(int, z, 3, !=);    
    ASSRT_OP(int, z, 1, >);
    ASSRT_OP(int, z, 3, <);
    ASSRT_OP(int, z, 2, >);
    return 0;
}