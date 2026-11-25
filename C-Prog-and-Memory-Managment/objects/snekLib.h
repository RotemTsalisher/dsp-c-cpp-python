#include <stdio.h>

/* forward declerations :*/

typedef enum   snek_kind     snek_kind_t;
typedef union  snek_data     snek_data_t;
typedef struct snek_object   snek_object_t;
typedef struct snek_vector   snek_vector_t;
typedef struct snek_array    snek_array_t;

/*                       */

/* structs and type definitions start */

enum snek_kind {
    INT,
    FLOAT,
    STR,
    VECTOR, 
    ARRAY
};

union snek_data {
    int int_v;
    float float_v;
    char *string_v;
    snek_vector_t vector_v;
    snek_array_t array_v;
};

struct snek_object {
    enum snek_kind type;
    union snek_data data;
};

struct snek_vector {
    snek_object_t *x;
    snek_object_t *y;
    snek_object_t *z;
};

struct snek_array {
    int size;
    snek_object_t** arr;
};

/* structs and type definitions end */

/* function declerations */

snek_object_t* new_snek_int(const int value);
snek_object_t* new_snek_float(const float value);
snek_object_t* new_snek_string(const char* value);
snek_object_t* new_snek_vector(snek_object_t* x_, snek_object_t* y_, snek_object_t* z_);
snek_object_t* new_snek_array(int size);