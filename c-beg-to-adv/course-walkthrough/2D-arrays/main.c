#include <stdio.h>
#include <stdlib.h>

#define ROWS 3
#define COLS 2


int main() {

    int nums[ROWS][COLS] = {
        {1, 2},
        {3, 4},
        {5, 6}
    };

    for (int i = 0; i<ROWS; ++i) {
        for(int j = 0; j < COLS ; ++j) {
            printf("| %d ", nums[i][j]);
        }
        printf("|\n");
    };
    return 0;
}