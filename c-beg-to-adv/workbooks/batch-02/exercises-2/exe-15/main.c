#include <stdio.h>
#include <stdlib.h>

#define ROWS 5
#define COLS ROWS
int main() {

    for(int i = 0; i < ROWS; ++i) {
        for(int j = 0; j < COLS; ++j) {
            if( ((i%2 == 0) && (j%2 != 0)) || ((j%2 ==0) && (i%2 != 0) ) ){
                printf("| . |");
            }
            else {
                printf("| X |");
            }
        }
        printf("\n");
    };
    return 0;
}