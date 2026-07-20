#include <stdio.h>
#include <stdlib.h>

struct Row {
    int id;
    double p;
};

int write_session(const char *path, const struct Row *r, int n);

#define MAX_ARR_SIZE               10
#define WRITE_ROW_FMT(id, power)   "%d,%lf\n",id,power
#define FILE_PATH                  "../log.csv"

int main() {

    int n = -1;
    struct Row rows[MAX_ARR_SIZE];

    printf("Enter amount of rows : ");
    scanf("%d", &n);

    for(int i = 0; i < n; ++i){
        printf("Enter id, power pair : ");
        scanf("%d %lf", &(rows[i].id), &(rows[i].p));
    }

    write_session(FILE_PATH, rows, n);
    return 0;
}

int write_session(const char *path, const struct Row *r, int n) {
    
    FILE* pFile = fopen(path, "a");

    if(!pFile) {
        return -1;
    }
    for(int i = 0; i < n; ++i) {
        if(0 > fprintf(pFile, WRITE_ROW_FMT(r[i].id, r[i].p))) {
            return -1;
        }
    }

    fclose(pFile);
    printf("DONE!\n");
    return 0;
}
