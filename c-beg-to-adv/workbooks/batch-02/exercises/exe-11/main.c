#include <stdio.h>
#include <stdlib.h>

#define FFT_LEN 512
#define HOP     128
#define FS      48000

int main() {

    const int OVERLAP = FFT_LEN - HOP;
    const double FRAME_MS = FFT_LEN / ((double)FS);

    printf("FFT LEN : %03d | HOP SIZE : %03d | FS : %05d | OVERLAP : %03d | FRAME MS : %5.3f |\n", FFT_LEN, HOP, FS, OVERLAP, FRAME_MS);
    return 0;
}