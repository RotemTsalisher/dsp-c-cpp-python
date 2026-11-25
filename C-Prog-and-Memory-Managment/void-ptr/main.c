#include <stdio.h>
#include "myLib.h"

int main() {

    snek_int_t snek_int;
    snek_float_t snek_float;
    snek_bool_t snek_bool;

    init_value((void*)&snek_int, INT);
    init_value((void*)&snek_float, FLOAT);
    init_value((void*)&snek_bool, BOOL);

    print_value((void*)&snek_int, INT);
    print_value((void*)&snek_float, FLOAT);
    print_value((void*)&snek_bool, BOOL);

    int int_val = 5;
    float float_val = 3.14;
    unsigned int bool_val = 1;

    set_value((void*)&snek_int, INT, (void*)&int_val);
    set_value((void*)&snek_float, FLOAT, (void*)&float_val);
    set_value((void*)&snek_bool, BOOL, (void*)&bool_val);

    print_value((void*)&snek_int, INT);
    print_value((void*)&snek_float, FLOAT);
    print_value((void*)&snek_bool, BOOL);

    return 0;
}