#include <stdio.h>


int main() {

    const unsigned int reg0 =0x000000A1 , reg1 = 0x80001234 , reg2 = 0xDEAD0000;

    printf("REG[%d] || raw = 0x%08X || low_byte = 0x%02X || msb_set = %c\n", 0, reg0, (reg0 & 0xFF), (0x10000000 & reg0) ? 'Y' : 'N');
    printf("REG[%d] || raw = 0x%08X || low_byte = 0x%02X || msb_set = %c\n", 1, reg1, (reg1 & 0xFF), (0x10000000 & reg1) ? 'Y' : 'N');
    printf("REG[%d] || raw = 0x%08X || low_byte = 0x%02X || msb_set = %c\n", 2, reg2, (reg2 & 0xFF), (0x10000000 & reg2) ? 'Y' : 'N');
    return 0;
}