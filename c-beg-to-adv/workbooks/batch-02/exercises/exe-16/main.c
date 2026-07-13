#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define OP_INIT_LEN   4
#define BIT_DEPTH     12
#define MAX_CHANNELS  3
#define MAX_FLAG_LEN  4
#define FULL_SCALE_V  2.5

#define AFE_MSG1   "========================================\n"
#define AFE_MSG2   "=========== AFE Bring Up V1 ============\n"
#define AFE_MSG    AFE_MSG1 AFE_MSG2 AFE_MSG1
#define CH_PRINT   "CH : %d | NAME : %3s | COUNTS : %d | VOLTS : %5.3lf | FLAG : %s\n"

struct channel_info {
    char name[OP_INIT_LEN], flag_[MAX_FLAG_LEN];
    int counts;
    double v;
};

void init_channel(struct channel_info *ci);
void print_channel(const struct channel_info *ci, int n);
void print_all_channels(const struct channel_info all_ch[], int size);

int main() {

    struct channel_info arr[MAX_CHANNELS];
    int num_ch;

    printf(AFE_MSG);

    printf("Enter number of channels [1-3] : ");
    scanf("%d", &num_ch);

    for(int i = 0; i<num_ch; i++) {
        init_channel(&(arr[i]));
    };

    print_all_channels(arr, num_ch);

    printf("DONE!\n");
    return 0;
}

void init_channel(struct channel_info *ci) {

    int name_init_idx = 0;

    printf("Enter Channel ID : ");
    scanf("%3s", ci->name);

    printf("Enter Counts : ");
    scanf("%d", &(ci->counts));

    ci->v = (ci->counts / (powf(2, BIT_DEPTH) - 1.0) ) * FULL_SCALE_V;

    if(ci->v >= 0.0 && ci->v <= 2.5) {
        ci->flag_[name_init_idx++] = 'O';
        ci->flag_[name_init_idx++] = 'K';
    }
    else {
        ci->flag_[name_init_idx++] = 'R';
        ci->flag_[name_init_idx++] = 'N';
        ci->flag_[name_init_idx++] = 'G';
    }
    ci->flag_[name_init_idx] = '\0';
};

void print_channel(const struct channel_info *ci, int n) {
    printf(CH_PRINT, n, ci->name, ci->counts, ci->v, ci->flag_);
};

void print_all_channels(const struct channel_info all_ch[], int size) {
    for(int i = 0; i < size; ++i) {
        print_channel(&(all_ch[i]), i);
    }
}