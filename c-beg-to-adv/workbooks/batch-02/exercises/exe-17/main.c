#include <stdio.h>
#include <stdlib.h>

#define CORRECT   'B'
#define GAME_MSG  "Unity Gain ? : A) %3.2lf B) %3.2lf C) %3.2lf D) %3.2lf\n"

int main() {

    double gA = 0.5, gB = 1.0, gC = 1.5, gD = 2.0;
    char pick = '?';

    printf(GAME_MSG, gA, gB, gC, gD);
    printf("Pick Answer : ");
    scanf(" %c", &pick);

    if(pick == CORRECT) {
        printf("WIN ! \n");
    }
    else{
        printf("LOSE ! \n");
    };

    return 0;
}