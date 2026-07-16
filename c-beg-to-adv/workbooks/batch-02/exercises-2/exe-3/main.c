#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define USER_MSG      "Enter Filter Type:\n\t1 - FLAT\n\t2 - COMB2\n\t4 - COMB4\n\t6 - ALL PASS\n"
#define OUT_MSG       "profile %d => %s taps %d\n"
#define MAX_NAME_SIZE 10

typedef enum {
    FLAT    = 0x01,
    COMB2   = 0x01<<1,
    COMB4   = 0x01<<2,
    ALLPASS = 0x06
}filter_type;

int main() {

    filter_type user_input;
    int taps = 0;
    char name_[MAX_NAME_SIZE] = {0};
    printf(USER_MSG);
    scanf("%d", &user_input);
    
    switch(user_input) {
        case FLAT:
            strcpy(name_, "FLAT");
            taps = 1;
            break;
        case COMB2:
            strcpy(name_, "COMB2");
            taps = 2;
            break;
        case COMB4: 
            strcpy(name_, "COMB4");
            taps = 4;
            break;
        case ALLPASS:
            strcpy(name_, "ALLPASS");
            taps = 6;
            break;
        default:
            printf("UNKNOWN!\n");
            return 0;
    }

    printf(OUT_MSG, user_input, name_, taps);
    return 0;
}