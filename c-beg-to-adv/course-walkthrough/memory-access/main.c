#include <stdio.h>
#include <stdlib.h>


int main() {

    int age = 30;
    int *p_age = &age;
    printf("address (p_age) = %p\n", p_age);
    printf("value = %d\n", *(p_age));
    return 0;
}