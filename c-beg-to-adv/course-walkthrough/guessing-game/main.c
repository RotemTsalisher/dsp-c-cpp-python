#include <stdio.h>
#include <stdlib.h>

#define SECRET_NUMBER    11
#define MAX_GUESS_COUNT  5
int main() {
    
    int guess, guess_count = 0, win_or_lose;

    while(guess != SECRET_NUMBER && guess_count++ < MAX_GUESS_COUNT) {
        printf("Enter a number : ");
        scanf("%d", &guess);
        win_or_lose = (guess == SECRET_NUMBER);
    };


    if(win_or_lose) {
        printf("CORRECT! SECRET NUMBER IS %d! YOU WIN!\n", SECRET_NUMBER);
    }
    else {
        printf("YOU RAN OUT OF GUESSES! BETTER LUCK NEXT TIME..\n");
    }
    return 0;
}