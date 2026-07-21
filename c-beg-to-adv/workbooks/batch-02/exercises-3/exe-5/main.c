#include <stdio.h>
#include <stdlib.h>

#define MAX_FRAMES_PER_FILE 64
#define MAX_BUFFER_SIZE     1024
#define SUCCESS             0
#define ROW_FMT(id, rms)    "%d,%lf\n",id,rms

int append_rms_row(FILE *fp, int frame_id, double rms);
int count_rows(const char *path);

static char buffer[MAX_BUFFER_SIZE];

int main() {

    int n = -1, id, amount_of_rows;
    double rms;

    FILE* pFile = fopen("../log.csv", "w");
    printf("Enter amount of lines : ");
    scanf(" %d", &n);

    for(int i = 0; i < n; ++i) {
        printf("Enter id, rms pair : ");
        scanf("%d %lf", &id, &rms);
        append_rms_row(pFile, id, rms);
    }

    fclose(pFile);

    printf("========= COUNTING ROWS ===========\n");
    amount_of_rows = count_rows("../log.csv");
    printf("ROWS : %d\n", amount_of_rows);
    return SUCCESS;
}

int append_rms_row(FILE *fp, int frame_id, double rms) {

    if(0 > fprintf(fp, ROW_FMT(frame_id, rms))) {
        return -1;
    };
    return SUCCESS;

};

int count_rows(const char *path) {
    int count_rows = 0;
    FILE* pFile = fopen(path, "r");

    while(fgets(buffer, MAX_BUFFER_SIZE, pFile)) {
        count_rows++;
    };

    return count_rows;
};