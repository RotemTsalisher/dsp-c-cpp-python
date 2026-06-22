#include <stdio.h>

int main() {

    int character_age = 34;
    const char* character_name = "Rotem";
    
    printf("There once was a man named %s\n", character_name);
    printf("He was %d years old.\n", character_age);
    printf("He really liked the name %s\n", character_name);
    printf("But did not like being %d.\n", character_age);
    
    return 0;
}