#include <stdio.h>
#include <stdlib.h>


int main() {

    int read = 0, sum = 0, count = 0;

    while(read != -1) {
        count++;
        sum += read;
        printf("Enter an integer : ");
        scanf(" %d", &read);
    };

    printf("n = %d | sum = %d\n", count, sum);
    return 0;
};
