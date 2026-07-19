#include <stdio.h>
#include <stdlib.h>

#define MAX_TAG_SIZE    10
#define ABS(v)          v > 0 ? v : -v
#define PRINT_FMT(f)    "Seq : %d | L : %4.2lf | R : %4.2lf | Tag : %s", f.seq, f.l, f.r, f.tag
#define PRINT_FRAME(f)  printf(PRINT_FMT(f))
#define FRAME_ARR_SIZE  3
struct Frame {
    int seq;
    double l,r;
    char tag[MAX_TAG_SIZE];
};

double frame_peak(const struct Frame *f);
void init_frame(struct Frame *f);

int main() {

    struct Frame frame_array[FRAME_ARR_SIZE];

    for (int i = 0; i <FRAME_ARR_SIZE; ++i) {
        init_frame(frame_array + i);
    };

    for (int i = 0; i < FRAME_ARR_SIZE; ++i) {
        PRINT_FRAME(frame_array[i]);
    };
    return 0;
}

double frame_peak(const struct Frame *f) {
    return ABS(f->l) > ABS(f->r) ? ABS(f->l) : ABS(f->r);
};

void init_frame(struct Frame *f) {
    
    printf("Enter Seq : ");
    scanf(" %d", &(f->seq));

    fgetc(stdin);
    printf("Enter Left Sample : ");
    scanf(" %lf", &(f->l));

    fgetc(stdin);
    printf("Enter Right Sample : ");
    scanf(" %lf", &(f->r));

    fgetc(stdin);
    printf("Enter Tag : ");
    fgets(f->tag, MAX_TAG_SIZE, stdin);
}