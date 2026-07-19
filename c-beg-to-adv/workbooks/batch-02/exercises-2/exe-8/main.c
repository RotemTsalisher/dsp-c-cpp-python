#include <stdio.h>
#include <stdlib.h>

#define STOP     0.0
#define CLIPPING 0.98

int main() {

    double read = 0.0, sum = 0.0;
    int count_clips = 0, max_streak = 0, tmp = 0;

    do {
        sum += read;
        printf("Enter float value : ");
        scanf(" %lf", &read);

        if(read > 0) {
            tmp++;
        }
        else {
            max_streak = (tmp > max_streak) ? tmp : max_streak;
            tmp = 0;
        };

        if(read > CLIPPING) {
            count_clips++;
        };
    }while(read != STOP);

    printf("Count Clips : %d | Max Streak : %d\n", count_clips, max_streak);
    return 0;
}