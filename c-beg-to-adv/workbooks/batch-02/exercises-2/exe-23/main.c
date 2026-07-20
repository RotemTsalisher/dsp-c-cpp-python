#include <stdio.h>
#include <stdlib.h>

#define FILE_PATH                       "../cal.txt"
#define WRITE_REG_LINE_FMT(addr, val)   "0x%08x = 0x%02x\n", addr, val 
#define WRITE_REG_LINE(addr, val, ptr)       fprintf(ptr, WRITE_REG_LINE_FMT(addr, val))

int main() {

    short reg0 = 0x01, reg1 = 0x02, reg2 = 0x03;
    FILE* pfile = fopen(FILE_PATH, "w");
    
    WRITE_REG_LINE(&reg0, reg0, pfile);
    WRITE_REG_LINE(&reg1, reg1, pfile);
    WRITE_REG_LINE(&reg2, reg2, pfile);

    fclose(pfile);
    return 0;
}