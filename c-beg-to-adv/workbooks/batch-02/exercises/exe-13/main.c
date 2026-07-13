#include <stdio.h>
#include <stdlib.h>

#define PRINT_FMT        "BOARD %04d PATH %c GAIN %+.1f dB @ %s"
#define CLEAN_INPU_BUFF  scanf("%c")
#define USER_PROMPT(s)   printf("Pleas Enter " #s " : ")
#define MAX_STRING_SIZE  40


int main() {

    int board_id;
    char path, site[MAX_STRING_SIZE];
    float gain_db;
    
    USER_PROMPT(Board ID);
    scanf("%d", &board_id);

    CLEAN_INPU_BUFF;
    USER_PROMPT(Path);
    scanf("%c", &path);

    USER_PROMPT(Gain [dB]);
    scanf("%f", &gain_db);

    CLEAN_INPU_BUFF;
    USER_PROMPT(Site);
    fgets(site, MAX_STRING_SIZE, stdin);

    printf(PRINT_FMT, board_id, path, gain_db, site);

    return 0;
}