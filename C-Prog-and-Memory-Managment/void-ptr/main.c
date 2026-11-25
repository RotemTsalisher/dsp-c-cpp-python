#include <stdio.h>
#include "myLib.h"

int main() {

    /*
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
    */

    /*
    char* str1 = "str1";
    char* str2 = "str2";

    printf("str1: %s || str2: %s\n", str1, str2);
    swap_strings(&str1, &str2);
    printf("str1: %s || str2: %s\n", str1, str2);
    */

    snek_int_t snek_int_a = { .val = 5, .name = "snek int a"};
    snek_int_t snek_int_b = {.val = 100, .name = "snek int b"};

    snek_float_t snek_float_a = { .val = 3.14, .name = "snek float a"};
    snek_float_t snek_float_b = {.val = 1.125, .name = "snek float b"};

    printf(" -- INT: --\n");

    print_value((void*)&snek_int_a, INT);
    print_value((void*)&snek_int_b, INT);

    printf(" -- SWAP! --\n");

    swap_structs((void*)&snek_int_a, (void*)&snek_int_b, sizeof(snek_int_t));

    print_value((void*)&snek_int_a, INT);
    print_value((void*)&snek_int_b, INT);

    printf(" -- FLOAT: --\n");
    
    print_value((void*)&snek_float_a, FLOAT);
    print_value((void*)&snek_float_b, FLOAT);

    printf(" -- SWAP! --\n");

    swap_structs((void*)&snek_float_a, (void*)&snek_float_b, sizeof(snek_float_t));

    print_value((void*)&snek_float_a, FLOAT);
    print_value((void*)&snek_float_b, FLOAT);
    return 0;
}