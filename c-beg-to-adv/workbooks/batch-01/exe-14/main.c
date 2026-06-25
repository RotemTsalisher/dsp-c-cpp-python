#include <stdio.h>
#include <stdlib.h>

#define SPECTRUM_SIZE 8
#define NAME_SIZE_MAX 50
#define COLD          "COLD"
#define WARM          "WARM"
#define HOT           "HOT"
#define MAX_TRIES     5

double bin_pwr(int k);
const char* hint_for(double guess_pwr, double peak_pwr);

static double spectrum[SPECTRUM_SIZE] = {0.01, 0.35, 0.45, 0.02, 0.85, 0.01, 0.15, 0.3};

int main() {

    char player_name[NAME_SIZE_MAX];
    int rounds = 0, players_guess;
    double guessed_power, peak_power = 0.85;

    printf("Enter player name : ");
    fgets(player_name, NAME_SIZE_MAX, stdin);

    printf("Ok, %s", player_name);
    while(rounds++ < MAX_TRIES) {
        printf("Guess the bin with the max psd value : ");
        scanf("%d", &players_guess);
        
        guessed_power = bin_pwr(players_guess);

        if(guessed_power == peak_power) {
            printf("SUCCESS!\n");
            return 0;
        }
        printf("%s !\n", hint_for(guessed_power, peak_power));
    }

    printf("COULDN'T GUESS CORRECTLY! BYE! \n");
    return 0;
}

double bin_pwr(int k) {
    return spectrum[k];
};
const char* hint_for(double guess_pwr, double peak_pwr) {
    double ratio = guess_pwr / peak_pwr;

    if(ratio > 0.0 && ratio < 0.25) {
        return COLD;
    }
    else if (ratio >= 0.25 && ratio <=0.5) {
        return WARM;
    }

    return HOT;
};