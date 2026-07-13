#include <stdio.h>
#include <stdlib.h>

#define OP_INIT_LEN 4

#define AFE_MSG1   "========================================\n"
#define AFE_MSG2   "=========== AFE Bring Up V1 ============\n"
#define AFE_MSG    AFE_MSG1 AFE_MSG2 AFE_MSG1

#define PRINT_MSG  "Operator Initials : %s | Operator Serial : %d | Operator Counts : %d | Operator Bits : %d |\n"

int main() {

    char op_init[OP_INIT_LEN];
    int counts, serial, bits;

    printf(AFE_MSG);
    
    printf("Enter Operator Initials : ");
    scanf("%3s", op_init);

    printf("Enter Operator Serial : ");
    scanf("%d", &serial);

    printf("Enter Counts : ");
    scanf("%d", &counts);

    printf("Enter Bits : ");
    scanf("%d", &bits);

    printf(PRINT_MSG, op_init, serial, counts, bits);
    printf("DONE!\n");
    return 0;
}