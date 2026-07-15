#include <stdio.h>
#include <stdlib.h>

#define SUCCESS 0

int main() {

    char mode = '?';
    int delay = -1;

    printf("Enter mode [L/M/H] : ");
    scanf(" %c", &mode);
    
    delay = (mode == 'L') * 2 + (mode == 'M') * 5 + (mode == 'H') * 9;
    printf("Delay : %d\n", delay);

    for(int i = 0; i < delay; ++i) {
        putchar('|');
    }
    putchar('\n');
    return SUCCESS;
}