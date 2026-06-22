#include <stdio.h>
#define DOUBLES

int main() {
#ifdef INTEGERS
    int num1, num2;
    printf("Enter first number : ");
    scanf("%d", &num1);

    printf("Enter second number : ");
    scanf("%d", &num2);

    printf("%d + %d = %d\n", num1, num2, num1 + num2);
#else
    double num1, num2;
    printf("Enter first number : ");
    scanf("%lf", &num1);

    printf("Enter second number : ");
    scanf("%lf", &num2);

    printf("%.2lf + %.2lf = %.2lf\n", num1, num2, num1 + num2);
#endif
    return 0;
}