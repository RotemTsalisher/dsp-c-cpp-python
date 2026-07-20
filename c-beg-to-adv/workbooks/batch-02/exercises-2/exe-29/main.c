#include <stdio.h>
#include <stdlib.h>

#define FILE_PATH "../../exe-25/log.csv"

#define MAX_BUFF_SIZE 1024
static char buffer[MAX_BUFF_SIZE];

int main() {

    int line_count = 0;

    FILE* pFile = fopen(FILE_PATH, "r");

    while(fgets(buffer, MAX_BUFF_SIZE, pFile) != NULL) {
        line_count++;
    };

    printf("Lines : %d\n", line_count);

    fclose(pFile);
    return 0;
}