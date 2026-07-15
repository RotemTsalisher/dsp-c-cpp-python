#include <stdio.h>
#include <stdlib.h>

#define MAG(x) (x > 0.0 > x : -x)
#define REPEAT 5

int main() {

    int clips = 0, reduces = 0;
    double mag = 0.0;

    for(int i = 0; i < REPEAT; ++i) {
        printf("Enter Magnitude : ");
        scanf("%lf", &mag);

        if(mag > 1.0) {
            clips++;
            printf("CLIP!\n");
        }
        else if(mag > 0.85) {
            reduces++;
            printf("REDUCE!\n");
        }
        else if(mag > 0.5) {
            printf("WATCH!\n");
        }
        else {
            printf("OK!\n");
        }
    }

    printf("Amount of Clips %d | Amount of Reduces %d | \n", clips, reduces);
    return 0;
}