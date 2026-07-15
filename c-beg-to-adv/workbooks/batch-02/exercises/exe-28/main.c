#include <stdio.h>
#include <stdlib.h>

#define IN_RANGE(s)        (s<= 1.0 && s >=-1.0)
#define IS_POS_MULT(l, r)  (l * r >= 0.0)
#define IN_PHASE_OK(l, r)  (IN_RANGE(l) && IN_RANGE(r) && (IS_POS_MULT(l,r)))
#define MAG(s)             (s >= 0.0 ? s : -s)
#define LEVEL_OK(l, r)     ((MAG(l) <= 0.95) && (MAG(r) <= 0.95))

int main() {

    double l = 0.0, r = 0.0;
    int in_phase_flag = 0, levels_flag = 0;
    printf("Left Sample : ");
    scanf("%lf", &l);
    printf("Right Sample : ");
    scanf("%lf", &r);

    if (IN_PHASE_OK(l, r)) {
        in_phase_flag = 1;
        printf("IN PHASE OK!\n");
    }

    if (LEVEL_OK(l, r)) {
        levels_flag = 1;
        printf("LEVELS OK!\n");
    }

    if(in_phase_flag && levels_flag) {
        printf("PASS!\n");
    }
    else if(in_phase_flag == 0) {
        printf("NOT IN PHASE!\n");
    }
    else if(levels_flag == 0) {
        printf("NOT IN THE LEGAL LEVELS!\n");
    }


    return 0;
}