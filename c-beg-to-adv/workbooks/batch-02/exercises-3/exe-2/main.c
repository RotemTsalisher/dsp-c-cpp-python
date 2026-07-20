#include <stdio.h>
#include <stdlib.h>

int main() {

    int offset, counts;
    double gain;
    char site[40] = {0};

    printf("Enter : offset counts gain site ");
    scanf("%d %d %lf", &offset, &counts, &gain);
    getchar();

    fgets(site, 40, stdin);

    printf("ECHO: %d %d %4.2lf %s", offset, counts, gain, site);
    return 0;
}