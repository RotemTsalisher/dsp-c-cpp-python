#include <stdio.h>
#include <stdlib.h>


#define BUFFER_SIZE 1024
static char buffer[BUFFER_SIZE];

int main() {

    FILE* pFile = fopen("../cal.txt", "r");

    fgets(buffer, BUFFER_SIZE, pFile);

    printf("BUFFER : %s\n", buffer);
    return 0;
}