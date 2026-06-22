#include <stdio.h>

int main() {

    int lucky_numbers[7] = {
        4, 8, 16, 23 ,42
    };

    lucky_numbers[5] = 100;
    lucky_numbers[6] = -2;
    printf("%d\n", lucky_numbers[6]);
    return 0;
}