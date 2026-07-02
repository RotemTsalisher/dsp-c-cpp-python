#include <stdio.h>
#include <stdlib.h>

#define N 9

unsigned int abs_(int num);
void print_row(int tap);

int main() {


    for(int i = 0; i < N; ++i) {
        print_row(i);
    };
    return 0;
};

unsigned int abs_(int num) {
    if (num < 0){
        return -num;
    };
    return num;
};

void print_row(int tap) {

    int len = 10 - abs_(4 - tap);
    printf("Tap %d | ", tap);
    for(int i = 0; i< len; ++i) {
        printf("=");
    };
    printf("\n");
};