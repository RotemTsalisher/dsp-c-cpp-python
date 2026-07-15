#include <stdio.h>
#include <string.h>

#define PEAK 20
#define SIZE 6
static double tap_gains[SIZE] = {0.0};

int main() {

    int n = -1, bar = 0;
    double max_val = tap_gains[0];

    while(n < 1 || n > 6) {
        printf("enter size [1 - 6] : ");
        scanf("%d", &n);
    }
    
    for(int i = 0; i < n; ++i) {
        printf("val for tap_gains[%d] : ", i);
        scanf("%lf", &(tap_gains[i]));

        if(tap_gains[i] > max_val) {
            max_val = tap_gains[i];
        };
    }

    printf("===== ECHO ARRAY ======\n");
    for(int i = 0; i < n; ++i) {
        printf("tap_gains[%d] : %5.3lf | ", i, tap_gains[i]);
        bar = (tap_gains[i] / max_val) * 20;
        for(int k = 0 ; k < bar; ++k, putchar('*'));
        printf("\n");
    }
    printf("======================\n");
    return 0;
}