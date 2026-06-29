#include <stdio.h>

int max_(int a, int b) {
    if (a > b) {
        return a;
    };
    return b;
};

int max3(int a, int b, int c) {
    if(a > b && a > c) {
        return a;
    };
    if(b > a && b > c) {
        return b;
    };
    return c;
};

int main() {

    int a,b,c;
    printf("Enter a : ");
    scanf("%d", &a);

    printf("Enter b : ");
    scanf("%d", &b);

    printf("Enter c : ");
    scanf("%d", &c);

    printf("max3(%d, %d, %d) = %d\n", a, b, c, max3(a,b,c));

    return 0;
};