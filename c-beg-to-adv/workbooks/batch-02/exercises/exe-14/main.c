#include <stdio.h>
#include <stdlib.h>

#define MAX_N 8

int main() {

    int n = 0, ids[MAX_N];
    
    double v[MAX_N];

    for(int i = 0; i < MAX_N; ++i) {
        n = 0;
        while((n < 1) || (n > 8)) {
            printf("Enter value for n [1, 8] : ");
            scanf("%d", &n);
        };
        ids[i] = n;
        printf("Enter value for v : ");
        scanf("%lf", &(v[i]));
    };

    printf("----------------------\n");
    for(int i = 0; i < MAX_N; ++i) {
        printf("ids[%d] = %d | v[%d] = %5.3lf |\n", i, ids[i], i, v[i]);
    };
    return 0;
}