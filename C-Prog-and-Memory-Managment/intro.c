#include <stdio.h>

#define CALL_FUNC(type, op, a , b)  type ## _ ## op(a, b) 

#define INIT_UNION(val, un) \
    _Generic((val), \
        int: (un).i = (val), \
        float: (un).f = (val) \
    )

#define PRINT_UNION(type, un) \
    _Generic((type), \
        int: printf("Union value: %d\n", (un).i), \
        float: printf("Union value: %f\n", (un).f) \
    )


struct packed_data {
    char letter;
    int int_data; 
    float float_data;
};

struct coordinate_3d {
    float x, y, z;
};

union int_or_float {
    int i;
    float f;
};

typedef union int_or_float int_or_float_t;


typedef struct packed_data packed_data_t;
typedef struct coordinate_3d coordinate_3d_t;

void init_coordinate_3d_in_place(coordinate_3d_t *c);
coordinate_3d_t init_coordinate_3d_zero();
coordinate_3d_t init_coordinate_3d(float x, float y, float z);
coordinate_3d_t scale_coordinate_3d(coordinate_3d_t c, float scaler);

int int_add(int a, int b);
float float_add(float a, float b);
int int_mult(int a, int b);
float float_mult(float a, float b);

int main() {

    union int_or_float u1, u2;
    INIT_UNION(10, u1); 
    INIT_UNION(3.14f, u2);

    PRINT_UNION(u1.i, u1);
    PRINT_UNION(u2.f, u2);
    return 0;
};

void init_coordinate_3d_in_place(coordinate_3d_t *c) {
    c->x = 0.0f;
    c->y = 0.0f;
    c->z = 0.0f;
};

coordinate_3d_t init_coordinate_3d_zero() {
    coordinate_3d_t c = {
        .x = 0.0f,
        .y = 0.0f,
        .z = 0.0f
    };

    return c;
};

coordinate_3d_t init_coordinate_3d(float x, float y, float z) {
    coordinate_3d_t c = {
        .x = x,
        .y = y, 
        .z = z
    };

    return c;
};

coordinate_3d_t scale_coordinate_3d(coordinate_3d_t c, float scaler) {
    coordinate_3d_t scaled_c = {
        .x = c.x * scaler,
        .y = c.y * scaler,
        .z = c.z * scaler
    };

    return scaled_c;
};

int int_add(int a, int b) {
    return a + b;
};

float float_add(float a, float b) {
    return a + b;
};

int int_mult(int a, int b) {
    return a * b;
};

float float_mult(float a, float b) {
    return a * b;
};