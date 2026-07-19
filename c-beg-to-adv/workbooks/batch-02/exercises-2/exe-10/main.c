#include <stdio.h>
#include <stdlib.h>

#define MAX_CAPTURE_SIZE           8 
#define PRINT_PAIR_FMT(ie, ve)     "ID : %d | Power : %4.2lf |\n", ie, ve
#define PRINT_PAIR(ie, ve)         printf(PRINT_PAIR_FMT(ie, ve))  
#define INIT_FILE_FMT              "========== SESSION.TXT ==========\n"
#define CLOSING_FILE_FMT           "=================================\n"
#define FILE_DUMP(pfile, ie, ve)   fprintf(pfile, PRINT_PAIR_FMT(ie, ve))
#define MAX_LINE_SIZE              1024

static char line_dump[MAX_CAPTURE_SIZE] = {0};
void print_pairs(const int *idx_arr, const double *power_arr, int size);
int lines_read(FILE* pfile);

int main() {

    int m, n = -1;
    int idx_array[MAX_CAPTURE_SIZE] = {0};
    double power_array[MAX_CAPTURE_SIZE] = {0.0};
    FILE* pfile = fopen("../session.txt", "w");

    if(!pfile) {
        printf("ERROR OPENING FILE!\n");
        exit(1);
    }

    fprintf(pfile, INIT_FILE_FMT);

    printf("Enter n : ");
    scanf(" %d", &n);
    fprintf(pfile, "n = %d\n", n);

    for(int i = 0; i < n; ++i) {
        printf("Enter index, power pair : ");
        scanf("%d %lf", idx_array + i, power_array + i);
        FILE_DUMP(pfile, idx_array[i], power_array[i]);
    }

    fprintf(pfile, CLOSING_FILE_FMT);
    fclose(pfile);


    // read lines :

    pfile = fopen("../session.txt", "r");
    m = lines_read(pfile);

    printf("READ = %d | WROTE = %d |\n", m, n);
    if(m == n) {
        printf("MATCH!\n");
    }
    return 0;
}

void print_pairs(const int *idx_arr, const double *power_arr, int size) {
    for(int i = 0; i < size; ++i) {
        PRINT_PAIR(idx_arr[i], power_arr[i]);
    };
};

int lines_read(FILE* pfile) {

    int line_count = 0;
    while(fgets(line_dump, MAX_LINE_SIZE, pfile) != NULL) {
        line_count++;
    };

    // subtract the first two line (just headers) and last closing line
    return line_count - 2 - 1;
};