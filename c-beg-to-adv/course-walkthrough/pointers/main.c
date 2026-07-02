#include <stdio.h>
#include <stdlib.h>


int main() {
    int age = 30;
    int *p_age = &age;

    double gpa = 3.4;
    double *p_gpa = &gpa;

    char grade = 'A';
    char *p_grade = &grade;

    printf("int value at address = 0x%p is : %d\n", p_age, *p_age);
    printf("double value at address = 0x%p is : %5.3lf\n", p_gpa, *p_gpa);
    printf("char value at address = 0x%p is : %c\n", p_grade, *p_grade);
    return 0;
}