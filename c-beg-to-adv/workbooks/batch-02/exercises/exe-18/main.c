#include <stdio.h>
#include <stdlib.h>

#define SIZE          8
#define MAX_NAME_SIZE 50


static double bin_powers[SIZE] = {
    12.5, 4.2, 27.8, 9.1,
    15.6, 33.4, 7.3, 21.0
};

int main() {

    char player_name[MAX_NAME_SIZE];
    int idx_read = -1, idx_max = 5, turns_left = 20;

    while(idx_read != idx_max && turns_left > 0) {
        printf("Guess an index for max val [0-7] : ");
        scanf("%d", &idx_read);

        if(idx_read < idx_max) {
            printf("LOW!\n");
        }
        else if (idx_read > idx_max) {
            printf("HIGH!\n");
        }
        else if (idx_read == idx_max) {
            printf("FOUND! || score : %d\n", turns_left * 100);
        }
        turns_left--;
    }
    return 0;
}