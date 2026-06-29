#include <stdio.h>
#include <stdlib.h>

#define MAX_LOOPS 5

int main() {
    int i = 1;

    /*
    while(i <= MAX_LOOPS) {
        printf("%d\n", i++);
    };*/

    i = 1;
    do {
        printf("%d\n", i++);
    }while(i <= MAX_LOOPS);

    return 0;
};