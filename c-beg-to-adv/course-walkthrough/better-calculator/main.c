#include <stdio.h>

double calc_op(double a, double b, char op);

int main() {

    double a,b;
    char op;

    printf("Enter a number : ");
    scanf("%lf", &a);

    printf("Enter an operation (+, -, *, /): ");
    scanf(" %c", &op);

    printf("Enter a number : ");
    scanf("%lf", &b);

    printf("result = %5.3lf\n", calc_op(a,b,op));

    return 0;
}

double calc_op(double a, double b, char op) {
    if(op == '+') {
        return a + b;
    }
    if(op == '-') {
        return a - b;
    };
    if(op == '*') {
        return a * b;
    };
    return a / b;
};