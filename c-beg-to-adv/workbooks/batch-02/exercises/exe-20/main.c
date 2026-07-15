#include <stdio.h>
#include <stdlib.h>

#define PRINT_MSG "frame %3d | ch %c | hash %04X\n"

//` where hash is `(fid[i]*31 + ch[i]) & 0xFFFF

int main() {

    char ch[5] = {'L','R','L','R','L'};
    int fid[5] = {10,10,11,11,12};

    for(int i = 0; i < 5 ; ++i) {
        printf(PRINT_MSG, fid[i], ch[i], ((fid[i]*31 + ch[i]) & 0xFFFF));
    };
    return 0;
}