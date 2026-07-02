#include <stdio.h>
#include <stdlib.h>

void add_line(FILE * p_file, const char * line);
int main() {

    FILE * p_file = fopen("../files/new-file.txt", "w");

    add_line(p_file, "hello world!\n");
    add_line(p_file, "This is my first file.\n");
    fclose(p_file);
    return 0;
}

void add_line(FILE * p_file, const char * line){
    fprintf(p_file,line);
    printf("wrote to file: %s", line);
};