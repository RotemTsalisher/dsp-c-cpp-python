#include <stdio.h>
#include <stdlib.h>

#define SIZE 5
static int buffer[SIZE] = {1,2,3,4,5};

int main() {

    int *left = buffer;
    int *right = buffer + SIZE - 1;
    int *tmp;

    for(int i = 0; i < SIZE; ++i) {
        printf("| %d | ", buffer[i]);
    };
    printf("\n");

    while(left < right) {
        *tmp = *left;
        *left = *right;
        *right = *tmp;
        left++;
        right--;
    };

    for(int i = 0; i < SIZE; ++i) {
        printf("| %d | ", buffer[i]);
    };
    printf("\n");
    return 0;
}