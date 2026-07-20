#include <stdio.h>
#include <stdlib.h>


void init_csv_file();
void add_rows(int n);

#define FILE_PATH                   "../log.csv"
#define HEADER_FMT                  "id,power\n"
#define WRITE_ROW_FMT(id, power)    "%d,%lf\n", id, power 

int main() {

    int n = -1;
    
    printf("Enter amount of rows : ");
    scanf(" %d", &n);

    init_csv_file();
    add_rows(n);

    printf("DONE!\n");
    return 0;
}

void init_csv_file() {
    FILE* pfile = fopen(FILE_PATH, "w");

    fprintf(pfile, HEADER_FMT);

    fclose(pfile);
};

void add_rows(int n) {
    
    FILE* pfile = fopen(FILE_PATH, "a");

    int id = 0;
    double power = 0.0;
    
    for(int i = 0; i <n; ++i) {
        printf("Enter id, power pair : ");
        scanf("%d %lf", &id, &power);
        fprintf(pfile, WRITE_ROW_FMT(id, power));
    }    

    fclose(pfile);
}