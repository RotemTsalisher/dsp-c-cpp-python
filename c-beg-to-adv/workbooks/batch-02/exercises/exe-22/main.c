#include <stdio.h>
#include <stdlib.h>

#define MAX_N     8
#define TOKEN_LEN 4

static char channel_names[MAX_N][TOKEN_LEN] = {'\0'};
static int  offs[MAX_N];

int main() {

    int amount_of_channels = -1;
    int mapping[MAX_N] = {0};
    
    printf("Enter amount of channels [1-8] : ");
    scanf("%d", &amount_of_channels);

    for(int i = 0; i < amount_of_channels; ++i) {
        printf("Enter channel %d name (3 letter token) : ", i + 1);
        scanf("%c");
        fgets(channel_names[i], TOKEN_LEN, stdin);

        printf("Enter Offset : ");
        scanf("%d", &(offs[i]));
        mapping[offs[i]-1] = i;
    }

    printf("==========\n");
    for(int i = 0; i < amount_of_channels; ++i) {
        printf("%d : %-3s\n", i + 1, channel_names[mapping[i]]);
    };

    return 0;
}