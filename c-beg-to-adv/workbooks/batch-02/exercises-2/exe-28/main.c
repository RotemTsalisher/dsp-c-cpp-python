#include <stdio.h>
#include <stdlib.h>

#define FILE_PATH     "../../exe-25/log.csv"

#define MAX_BUFF_SIZE 1024
static char buffer[MAX_BUFF_SIZE];

int main() {

    FILE* pFile = fopen(FILE_PATH, "r");
    fgets(buffer, MAX_BUFF_SIZE, pFile);
    fgets(buffer, MAX_BUFF_SIZE, pFile);

    printf("BUFFER : %s\n", buffer);

    fclose(pFile);
    return 0;
}