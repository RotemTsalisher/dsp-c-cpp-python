#include <stdio.h>

/* forward declerations :*/

typedef struct snek_object   snek_object_t;
typedef struct snek_vector   snek_vector_t;

/*                       */

/* structs and type definitions start */

enum snek_kind {
    INT,
    FLOAT,
    STR,
    VECTOR
};

union snek_data {
    int int_v;
    float float_v;
    char *string_v;
    snek_vector_t vector_v;
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

typedef enum   snek_kind     snek_kind_t;
typedef union  snek_data     snek_data_t;
typedef struct snek_object   snek_object_t;
typedef struct snek_vector   snek_vector_t;

/* structs and type definitions end */

/* function declerations */

snek_object_t* new_snek_int(const int value);
snek_object_t* new_snek_float(const float value);
snek_object_t* new_snek_string(const char* value);
snek_vector_t* new_snek_vector(snek_object_t* x_, snek_object_t* y_, snek_vector_t* z_);