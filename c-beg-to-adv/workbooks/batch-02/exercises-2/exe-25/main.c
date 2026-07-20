#include <stdio.h>
#include <stdlib.h>

int write_row(FILE* fp, int id, double power);

#define FILE_PATH          "../log.csv"
#define SUCCESS            0
#define HEADER             "id, power\n"
#define ROW_FMT(id, pwr)   "%d,%lf\n",id,pwr

int main() {

    FILE* pfile = fopen(FILE_PATH, "w");
    int n = -1, id = 0;
    double power = 0.0;

    fprintf(pfile, HEADER);
    printf("Enter amount of rows : ");
    scanf(" %d", &n);

    for(int i = 0; i < n; ++i) {
        printf("Enter id, power pair : ");
        scanf("%d %lf", &id, &power);
        if(0 > write_row(pfile, id, power)) {
            printf("ERROR WRITING ROW!\n");
            exit(1);
        }
    }

    fclose(pfile);
    printf("DONE!\n");
    return SUCCESS;
}

int write_row(FILE* fp, int id, double power) {
    if(0 > fprintf(fp, ROW_FMT(id, power))) {
        return -1;
    }
    return SUCCESS;
};