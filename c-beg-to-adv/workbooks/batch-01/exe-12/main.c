#include <stdio.h>
#include <stdlib.h>

static char reg_names[5][20];
static unsigned int reg_values[5];

void print_reg_table(char names[][20], unsigned int const *vals, int n);
unsigned int decode_gain_field(unsigned int raw);

int main() {
    reg_names[0][0] = 'G'; reg_names[0][1] = '1'; reg_names[0][2] = '\0';
    reg_names[1][0] = 'G'; reg_names[1][1] = '2'; reg_names[1][2] = '\0';
    reg_names[2][0] = 'G'; reg_names[2][1] = '3'; reg_names[2][2] = '\0';
    reg_names[3][0] = 'G'; reg_names[3][1] = '4'; reg_names[3][2] = '\0';
    reg_names[4][0] = 'G'; reg_names[4][1] = '5'; reg_names[4][2] = '\0';

    unsigned int raw_vals[5] = {
        0x1234, 0xABCD, 0x00FF, 0x5500, 0xFFFF
    };

    for(int i = 0; i < 5; ++i)
        reg_values[i] = decode_gain_field(raw_vals[i]);

    print_reg_table(reg_names, reg_values, 5);

    return 0;
}

void print_reg_table(char names[][20], unsigned int const *vals, int n) {
    for(int i = 0; i < n; ++i) {
        printf("reg |%s| = 0x%x\n", names[i], vals[i]);
    };
};

unsigned int decode_gain_field(unsigned int raw) {
    unsigned char res = (raw >> 8);
    return (unsigned int)res;
};
