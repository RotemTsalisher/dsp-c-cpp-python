#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>


#define HEADER               "===== AFE CAPTURE =====\n"
#define PRINT_FMT(i, v)      "Index : <%d> | Value : <%4.2lf>\n", i, v
#define PRINT_ROW(i, v)      printf(PRINT_FMT(i,v))
#define PRINT_HEADER         printf(HEADER)
#define PRINT_LENGTH(n)      printf("===== LENGTH: %d =====\n", n)      

#define SIZE 8
static double buffer[SIZE] = {
    0.1, -0.25, 0.4, 0.0, -0.15, 0.55, -0.05, 0.2
};


int main() {

    PRINT_HEADER;
    for(int i = 0; i < SIZE; ++i) {
        PRINT_ROW(i, buffer[i]);
    }
    PRINT_LENGTH(SIZE);
    return 0;
}



