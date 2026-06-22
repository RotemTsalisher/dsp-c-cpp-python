#include <stdio.h>
#include <stdlib.h>


float pow(int a, int b) {
    int i = 0;
    float res = 1.0;
    for(i; i<b; ++i, res *= a);
    return res;
}
int main() {

    printf("%.2f\n",5 * 4.5 );
    printf("%.2f\n", 4 / 5.0);

    printf("%.2f\n", pow(2,3));
    return 0;
}