#include <stdio.h>
#include <math.h>


#define CALL_FUNC(type, op, a , b)  type ## _ ## op(a, b) 
#define MAX_NUM ((0x01ULL<<32) - 1)

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

union age_or_name {
    int age;
    char* name;
};

enum union_type {
    AGE_TYPE,
    NAME_TYPE,
};

struct data_node {
    union age_or_name data;
    enum union_type type;
};

union int_and_unsigned {
    int i;
    unsigned int _i;
};

typedef union int_or_float int_or_float_t;
typedef struct packed_data packed_data_t;
typedef struct coordinate_3d coordinate_3d_t;
typedef union age_or_name age_or_name_t;
typedef enum union_type union_type_t;
typedef struct data_node data_node_t;
typedef union int_and_unsigned int_and_unsigned_t;

void init_coordinate_3d_in_place(coordinate_3d_t *c);
coordinate_3d_t init_coordinate_3d_zero();
coordinate_3d_t init_coordinate_3d(float x, float y, float z);
coordinate_3d_t scale_coordinate_3d(coordinate_3d_t c, float scaler);
void print_data_node(data_node_t *node);

int int_add(int a, int b);
float float_add(float a, float b);
int int_mult(int a, int b);
float float_mult(float a, float b);

int main() {

    printf("sizeof(int) = %d\n", sizeof(int));
    int_and_unsigned_t i_and_u;
    i_and_u.i = -1;

    printf("i_and_u.i = %d\n", i_and_u.i);
    printf("i_and_u._i = %u\n", i_and_u._i);
    printf("MAX_NUM = %llu\n", (unsigned long long)(MAX_NUM));
    return 0;
};


void print_data_node(data_node_t *node) {
    switch(node->type) {
        case NAME_TYPE:
            printf("Name: %s\n", node->data.name);
            break;
        case AGE_TYPE:
            printf("Age: %d\n", node->data.age);
            break;
        default:
            printf("Unknown type\n");
            break;
    }
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