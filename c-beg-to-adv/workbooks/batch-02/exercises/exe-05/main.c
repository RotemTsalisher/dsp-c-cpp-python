#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_NAME_SIZE 50

struct reg_dump {
    unsigned int addr;
    float temp_c;
    char bus_id;
    char name[MAX_NAME_SIZE];
};

void init_dump(struct reg_dump* rd);
void print_dump(const struct reg_dump* rd);

int main() {

    struct reg_dump rd;
    init_dump(&rd);
    print_dump(&rd);

    return 0;
};

void init_dump(struct reg_dump* rd) {
    
    rd->addr = 0x40001234;
    rd->temp_c = 37.5f;
    rd->bus_id = 'I';
    strcpy(rd->name, "SPI-AFE");
    return ;
}

void print_dump(const struct reg_dump* rd) {
    printf("ADDRESS : 0x%08X | ", rd->addr);
    printf("TEMPERATURE : %.1f | ", rd->temp_c);
    printf("BUS : %c | ", rd->bus_id);
    printf("NAME : %s |\n", rd->name);
    return;
}