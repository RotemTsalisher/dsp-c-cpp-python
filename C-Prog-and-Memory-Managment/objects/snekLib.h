#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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


struct snek_vector {
    snek_object_t *x;
    snek_object_t *y;
    snek_object_t *z;
};

struct snek_array {
    int size;
    snek_object_t** arr;
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

/* structs and type definitions end */

/* function declerations */

snek_object_t* new_snek_int(const int value);
snek_object_t* new_snek_float(const float value);
snek_object_t* new_snek_string(const char* value);
snek_object_t* new_snek_vector(snek_object_t* x_, snek_object_t* y_, snek_object_t* z_);
snek_object_t* new_snek_array(int size);

int snek_array_set(snek_object_t* obj, int index, snek_object_t* value);
snek_object_t* snek_array_get(const snek_object_t* obj, int index);

int snek_length(snek_object_t* obj);

snek_object_t* snek_add(const snek_object_t* a, const snek_object_t* b);
static inline snek_object_t* add_snek_int(const snek_object_t* a, const snek_object_t* b) {
    
    if(!(a) || !(b)) {
        return NULL;
    };

    if( (a->type != INT) || (b->type != INT)) {
        return NULL;
    };

    return new_snek_int(a->data.int_v + b->data.int_v);
}

static inline snek_object_t* add_snek_float(const snek_object_t* a, const snek_object_t* b) {
    
    if(!(a) || !(b)) {
        return NULL;
    };

    if( (a->type != FLOAT) || (b->type != FLOAT)) {
        return NULL;
    };

    return new_snek_float(a->data.float_v + b->data.float_v);
}

static inline snek_object_t* add_snek_string(const snek_object_t* a, const snek_object_t* b) {

    if(!(a) || !(b)) {
        return NULL;
    };

    if(!(a->data.string_v) || !(b->data.string_v)) {
        return NULL;
    };

    if((a->type != STR) || (b->type != STR)) {
        return NULL;
    };

    int str_len = strlen(a->data.string_v) + strlen(b->data.string_v) + 1;
    char* value = (char*)malloc(sizeof(char) * str_len);

    if(!(value)) return NULL;

    memset(value, 0, str_len);
    strcat(value, a->data.string_v);
    strcat(value, b->data.string_v);
    snek_object_t* obj = new_snek_string(value);

    free(value);
    return obj;
};

static inline snek_object_t* add_snek_vector(const snek_object_t* a, const snek_object_t* b) {
    
    if(!(a) || !(b)) return NULL;
    if((a->type != VECTOR) || (b->type != VECTOR)) return NULL;

    return new_snek_vector(
        snek_add(a->data.vector_v.x, b->data.vector_v.x),
        snek_add(a->data.vector_v.y, b->data.vector_v.y),
        snek_add(a->data.vector_v.z, b->data.vector_v.z)
    );
}
static inline snek_object_t* add_snek_array(const snek_object_t* a, const snek_object_t* b) {

    if(!(a) || !(b) ) return NULL;
    if((a->type != ARRAY) || (b->type != ARRAY)) return NULL;

    snek_object_t* new = new_snek_array(a->data.array_v.size + b->data.array_v.size);

    for(int i = 0; i < a->data.array_v.size; ++i) {
        snek_array_set(new, i, snek_array_get(a, i));
    };

    for(int i = 0; i < b->data.array_v.size; ++i) {
        snek_array_set(new, i + a->data.array_v.size, snek_array_get(b, i));
    };

    return new;
}