#include <stdio.h>
#include <stdlib.h>

#define MAX_LINE_SIZE 255

int main() {

    char line_[MAX_LINE_SIZE];
    FILE * p_file = fopen("../../writing-files/files/new-file.txt", "r");

    fgets(line_, MAX_LINE_SIZE, p_file);
    printf("read line : %s", line_);
    fgets(line_, MAX_LINE_SIZE, p_file);
    printf("read line : %s", line_);


    fgets(line_, MAX_LINE_SIZE, p_file);
    printf("read line : %s", line_);
    fgets(line_, MAX_LINE_SIZE, p_file);
    printf("read line : %s", line_);
    return 0;

}