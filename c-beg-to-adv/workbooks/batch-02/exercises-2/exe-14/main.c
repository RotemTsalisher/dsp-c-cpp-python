#include <stdio.h>
#include <stdlib.h>

#define ROWS 4
#define COLS ROWS

struct Coordinates {
    int i,j;
};

struct Coordinates find_max_coords(const double adc[ROWS][COLS], int r, int c);
void set_val(double arr[ROWS][COLS], int r, int c, double val);


static double adc[ROWS][COLS] = {
    {12.4,  8.1,  3.5,  9.7},
    { 5.2, 14.8,  7.6,  2.3},
    {11.1,  4.9, 16.5, 10.2},
    { 6.7, 13.3,  1.8, 15.0}
};

int main() {

    struct Coordinates max_coords = find_max_coords(adc, ROWS, COLS);
    set_val(adc, max_coords.i, max_coords.j, 0.0);

    printf("max coords : %d, %d\n", max_coords.i, max_coords.j);
    for(int i = 0; i < ROWS; ++i) {
        for(int j = 0; j < COLS; ++j) {
            printf("| %6.3lf |", adc[i][j]);
        }
        printf("\n");
    };


    return 0;
};

struct Coordinates find_max_coords(const double adc[ROWS][COLS], int r, int c) {
    double tmp = adc[0][0];
    struct Coordinates max = {0, 0};

    for(int i = 0; i < r; ++i) {
        for(int j = 0; j < c; ++j) {
            if(adc[i][j] > tmp) {
                tmp = adc[i][j];
                max.i = i;
                max.j = j;
            }
        }
    }

    return max;
};

void set_val(double arr[ROWS][COLS], int r, int c, double val) {
    arr[r][c] = val;
};
