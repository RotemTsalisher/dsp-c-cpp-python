#include <stdio.h>
#include <stdlib.h>

#define MAX_FRAMES 64
#define CHANNELS   2
#define TAG_LEN    8
#define PRINT_FORMAT "%-16s : %-6d\n"
#define PRINT(m, v) printf(PRINT_FORMAT, m, v)

int main() {

    const int frame_in_bytes  = CHANNELS * (int)sizeof(double) * TAG_LEN;
    const int buffer_in_bytes = frame_in_bytes * MAX_FRAMES;

    PRINT("FRAME IN BYTES", frame_in_bytes);
    PRINT("BUFFER IN BYTES", buffer_in_bytes);
    return 0;
}