#include <stdio.h>
#include <stdlib.h>

static int can_write(unsigned addr, unsigned val, int range_ok);

int main() {

    can_write(0x4000, 0x00FF, 1);
    can_write(0x4001, 0x00FF, 1);
    can_write(0x4000, 0x1FFFF, 1);
    return 0;
}

static int can_write(unsigned addr, unsigned val, int range_ok) {
    int aligned = (addr % 4u == 0);

    if(aligned && (val <=0xFFFF) && (range_ok != 0)) {
        printf("WRITE OK!\n");
        return 1;
    }

    printf("WRITING BLOCKED!\n");
    return 0;
}