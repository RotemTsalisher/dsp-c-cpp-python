#include <stdio.h>
#include <stdlib.h>

void print_row(char ch, int raw, double scaled);

int main() {

    char channel_a = 'A', channel_b = 'B', channel_c = 'C';
    int offset_a = 12, offset_b = -3, offset_c = 7;
    double factor_a = 1.0, factor_b = 0.5, factor_c = 2.0;

    double scaled_a = (double)offset_a * factor_a;
    double scaled_b = (double)offset_b * factor_b;
    double scaled_c = (double)offset_c * factor_c;

    print_row(channel_a, offset_a, scaled_a);
    print_row(channel_b, offset_b, scaled_b);
    print_row(channel_c, offset_c, scaled_c);
    return 0;
}
void print_row(char ch, int raw, double scaled) {
    printf("CH %c | raw = %d | scaled = %.2lf\n", ch, raw, scaled );
    return ;
};