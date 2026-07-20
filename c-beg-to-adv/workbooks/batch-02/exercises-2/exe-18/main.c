#include <stdio.h>
#include <stdlib.h>


int main() {
    unsigned char raw[8] = {
        0x34, 0x12,
        0x78, 0x56,
        0xBC, 0x9A,
        0xF0, 0xDE
    };

    unsigned short tmp = 0;
    unsigned short sum = 0;

    for(int i = 0; i < 8; i = i + 2) {
        tmp = (raw[i] | raw[i+1]<<8);
        printf("HEX : 0x%x | DEC : %d\n", tmp, tmp);
        sum += tmp;
    }
    printf("sum = %d\n", sum);
    return 0;
}