#include <stdio.h>
#include <stdlib.h>


int main() {

    double buff[6];

    unsigned char *p;
    p = (unsigned char *)buff;
    
    for(int i = 0; i <12; ++i, p++){ 
        printf("p = %p | *p = 0x%02x\n", p, *p);
    }

    p = (unsigned char *)buff;
    for(int i = 0; i <12; ++i){ 
        printf("p = %p | *p = 0x%02x\n", p, p[i]);
    }
    return 0;

    
    //return 0;
}