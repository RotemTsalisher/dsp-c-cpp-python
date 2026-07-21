#include <stdio.h>
#include <stdlib.h>


#define FILE_PATH        "../session.csv"
#define MAX_FRAMES       8
#define BINS_PER_FRAME   4
#define SUCCESS          0
#define MAX_BUFFER_SIZE  1024

#define ROW_FORMAT(frame)                 "%d,%lf,%lf,%lf,%lf\n",frame->frame_id, frame->bins[0], frame->bins[1], frame->bins[2], frame->bins[3]
#define PRINT_ROW_TO_FILE(frame, file)    fprintf(file, ROW_FORMAT(frame))
#define HEADER_FORMAT                     "id, bin 0, bin 1, bin 2, bin 3\n"
#define WRITE_HEADER(file)                fprintf(file, HEADER_FORMAT)

struct Frame {
    int frame_id;
    double bins[BINS_PER_FRAME];
};

static char buffer[MAX_BUFFER_SIZE];

int max_bin(const struct Frame *f);
int write_frame_to_csv(const struct Frame *f, FILE* pFile);
void print_peak_indices(FILE* pFile);

int main() {

    FILE* pFile = fopen(FILE_PATH, "w");
    int n = -1;
    struct Frame f;
    
    WRITE_HEADER(pFile);
    printf("Enter amount of frames : ");
    scanf(" %d", &n);

    for(int i = 0; i < n; ++i) {
        printf("Enter bin powers {id, bin0, bin1, bin2, bin3} : ");
        scanf("%d %lf %lf %lf %lf", &(f.frame_id), &(f.bins[0]), &(f.bins[1]), &(f.bins[2]), &(f.bins[3]));
        write_frame_to_csv(&f, pFile);
    };

    fclose(pFile);

    pFile = fopen(FILE_PATH, "r");
    print_peak_indices(pFile);
    fclose(pFile);

    printf("DONE!\n");
    return SUCCESS;
};

int max_bin(const struct Frame *f) {
    int max = f->bins[0];
    int max_idx = 0;
    for(int i = 1; i<BINS_PER_FRAME; ++i) {
        if(f->bins[i] > max) {
            max = f->bins[i];
            max_idx = i;
        };
    };

    return max_idx;
};

int write_frame_to_csv(const struct Frame *f, FILE* pFile) {
    if(0 > PRINT_ROW_TO_FILE(f, pFile)) {
        return -1;
    }
    return SUCCESS;
};

void print_peak_indices(FILE* pFile) {
    
    double max_val = -1000000000.0;
    int max_id = -1;
    int max_bin = -1;
    struct Frame f;

    fgets(buffer, MAX_BUFFER_SIZE, pFile); //discard first line

    while(fgets(buffer, MAX_BUFFER_SIZE, pFile)) {
        //printf("READING ROW... | %s |\n", buffer);
        sscanf(buffer, "%d,%lf,%lf,%lf,%lf", &(f.frame_id), &(f.bins[0]), &(f.bins[1]), &(f.bins[2]), &(f.bins[3]));
        for(int i =0; i<BINS_PER_FRAME; ++i){
            //printf("f.bins[%d] = %4.2lf | ", i, f.bins[i]);
            if(f.bins[i] > max_val) {
                max_val = f.bins[i];
                max_id = f.frame_id;
            }
        };
        //printf("\n");
    };

    printf("MAX ID : %d | MAX VAL : %4.2lf\n", max_id, max_val);
}