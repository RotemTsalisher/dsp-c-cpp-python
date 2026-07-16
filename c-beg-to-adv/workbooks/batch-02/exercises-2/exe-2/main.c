#include <stdio.h>
#include <stdlib.h>

#define PRINT_FMT "Mode : %c | Delay : %d | Gain 1 : %5.2lf | Gain 2 : %5.2lf | STATUS : 0x%x \n"

int main() {
    

    char mode = '?';
    int STATUS_, gain_one, gain_two, delay;
    double float_gain_one, float_gain_two;
    
    printf("Enter Mode [L/M/H] : ");
    scanf(" %c", &mode);

    printf("Enter Gain 1 [0-100] : ");
    scanf("%d", &gain_one);

    printf("Enter Gain 2 [0-100] : ");
    scanf("%d", &gain_two);

    float_gain_one = (float)gain_one / 100.0;
    float_gain_two = (float)gain_two / 100.0;

    switch(mode) {
        case 'L':
            delay = 2;
            break;
        case 'M':
            delay = 5;
            break;

        case 'H':
            delay = 9;
            break;
    }

    STATUS_ = (((float)gain_one + (float)gain_two) / 2.0 ) * (255.0 / 100.0) + 0.5;
    printf(PRINT_FMT, mode, delay, float_gain_one, float_gain_two, STATUS_);
    return 0;
}