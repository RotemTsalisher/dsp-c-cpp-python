#include <stdio.h>
#include <stdlib.h>

#define FILE_PATH             "../../exe-25/log.csv"
#define ABS(x)                (x > 0 ? x : -x)
#define MAX_BUFF_SIZE         1024
static char buffer[MAX_BUFF_SIZE];

int main() {

    FILE* pFile = fopen(FILE_PATH, "r");

    int id = 0;
    int max_id = id;
    double power = -100.0;
    double max_power = power;

    while(fgets(buffer, MAX_BUFF_SIZE, pFile)) {
        if(sscanf(buffer, "%d, %lf", &id, &power) == 2) {
            if(ABS(power) > max_power) {
                max_id = id;
                max_power = ABS(power);
            }
        }
    }
    printf("max id : %d | max power = %4.2lf\n", max_id, max_power);

    fclose(pFile);
    return 0;
}